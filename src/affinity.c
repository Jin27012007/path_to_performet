// Character affinity system (Lilycove opening).
//
// Each relevant character has an internal affinity in the range -100..+100.
// The value is stored in a save var as a signed delta from the character's
// initial value, so a freshly cleared save (var == 0) already holds the
// correct initial affinity and nothing has to be initialised at New Game.
//
// While a conversation is running, the script can show a small bar in the
// top-right corner. The bar never shows numbers, labels or evaluative colours;
// it simply fills proportionally and animates smoothly when the value changes.
//
// Script interface (see data/scripts/affinity.inc for macros):
//   VAR_0x8004 = AFFINITY_* character id
//   VAR_0x8005 = signed delta (for AffinityAdd)
//   special AffinityShowBar / AffinityAdd / AffinityHideBar / AffinityGet

#include "global.h"
#include "affinity.h"
#include "event_data.h"
#include "menu.h"
#include "task.h"
#include "window.h"
#include "constants/affinity.h"

#define BAR_WIN_LEFT    21
#define BAR_WIN_TOP     1
#define BAR_WIN_WIDTH   8
#define BAR_WIN_HEIGHT  1
#define BAR_BASE_BLOCK  0x30

#define BAR_X           4
#define BAR_Y           2
#define BAR_W           (BAR_WIN_WIDTH * 8 - BAR_X * 2)
#define BAR_H           4

// std menu palette indices (palette 15)
#define COL_BG          1
#define COL_FRAME       2
#define COL_EMPTY       3
#define COL_FILL        8
#define COL_SHINE       9

struct AffinityInfo
{
    u16 var;
    s8 initial;
};

static const struct AffinityInfo sAffinityInfo[AFFINITY_COUNT] =
{
    [AFFINITY_FATHER] = { .var = VAR_AFFINITY_FATHER, .initial = -10 },
};

// EWRAM data must be zero-initialised, so window/task ids are stored + 1 (0 = none).
static EWRAM_DATA u8 sBarWindowIdPlus1 = 0;
static EWRAM_DATA u8 sBarTaskIdPlus1 = 0;
static EWRAM_DATA u8 sBarCharacter = 0;

#define sBarWindowId ((u8)(sBarWindowIdPlus1 ? sBarWindowIdPlus1 - 1 : WINDOW_NONE))
#define sBarTaskId   ((u8)(sBarTaskIdPlus1 ? sBarTaskIdPlus1 - 1 : TASK_NONE))
#define SET_BAR_WINDOW(id) (sBarWindowIdPlus1 = ((id) == WINDOW_NONE) ? 0 : (id) + 1)
#define SET_BAR_TASK(id)   (sBarTaskIdPlus1 = ((id) == TASK_NONE) ? 0 : (id) + 1)

static void Task_AnimateBar(u8 taskId);

static s32 ClampAffinity(s32 value)
{
    if (value > AFFINITY_MAX)
        return AFFINITY_MAX;
    if (value < AFFINITY_MIN)
        return AFFINITY_MIN;
    return value;
}

s32 GetAffinity(u32 character)
{
    if (character >= AFFINITY_COUNT)
        return 0;
    return ClampAffinity(sAffinityInfo[character].initial + (s16)VarGet(sAffinityInfo[character].var));
}

void SetAffinity(u32 character, s32 value)
{
    if (character >= AFFINITY_COUNT)
        return;
    value = ClampAffinity(value);
    VarSet(sAffinityInfo[character].var, (u16)(s16)(value - sAffinityInfo[character].initial));
}

void AddAffinity(u32 character, s32 delta)
{
    SetAffinity(character, GetAffinity(character) + delta);
}

static u32 AffinityToPixels(s32 value)
{
    return ((value - AFFINITY_MIN) * BAR_W) / (AFFINITY_MAX - AFFINITY_MIN);
}

static void DrawBar(u32 fillPixels)
{
    if (sBarWindowId == WINDOW_NONE)
        return;
    FillWindowPixelBuffer(sBarWindowId, PIXEL_FILL(COL_BG));
    FillWindowPixelRect(sBarWindowId, PIXEL_FILL(COL_FRAME), BAR_X - 1, BAR_Y - 1, BAR_W + 2, BAR_H + 2);
    FillWindowPixelRect(sBarWindowId, PIXEL_FILL(COL_EMPTY), BAR_X, BAR_Y, BAR_W, BAR_H);
    if (fillPixels > 0)
    {
        FillWindowPixelRect(sBarWindowId, PIXEL_FILL(COL_FILL), BAR_X, BAR_Y, fillPixels, BAR_H);
        FillWindowPixelRect(sBarWindowId, PIXEL_FILL(COL_SHINE), BAR_X, BAR_Y, fillPixels, 1);
    }
    CopyWindowToVram(sBarWindowId, COPYWIN_GFX);
}

#define tShown   data[0]
#define tTarget  data[1]
#define tTimer   data[2]

static void Task_AnimateBar(u8 taskId)
{
    s16 *data = gTasks[taskId].data;

    if (sBarWindowId == WINDOW_NONE)
    {
        SET_BAR_TASK(TASK_NONE);
        DestroyTask(taskId);
        return;
    }
    if (tShown == tTarget || ++tTimer < 2)
        return;
    tTimer = 0;
    tShown += (tTarget > tShown) ? 1 : -1;
    DrawBar(tShown);
}

static void StartBarTask(u32 shown, u32 target)
{
    if (sBarTaskId == TASK_NONE)
        SET_BAR_TASK(CreateTask(Task_AnimateBar, 80));
    gTasks[sBarTaskId].tShown = shown;
    gTasks[sBarTaskId].tTarget = target;
    gTasks[sBarTaskId].tTimer = 0;
}

void ShowAffinityBar(u32 character)
{
    struct WindowTemplate template;
    u32 pixels;

    if (character >= AFFINITY_COUNT)
        return;
    sBarCharacter = character;
    pixels = AffinityToPixels(GetAffinity(character));
    if (sBarWindowId == WINDOW_NONE)
    {
        template = CreateWindowTemplate(0, BAR_WIN_LEFT, BAR_WIN_TOP, BAR_WIN_WIDTH, BAR_WIN_HEIGHT, 15, BAR_BASE_BLOCK);
        SET_BAR_WINDOW(AddWindow(&template));
        if (sBarWindowId == WINDOW_NONE)
            return;
        DrawStdWindowFrame(sBarWindowId, FALSE);
        PutWindowTilemap(sBarWindowId);
    }
    DrawBar(pixels);
    CopyWindowToVram(sBarWindowId, COPYWIN_FULL);
    StartBarTask(pixels, pixels);
}

void HideAffinityBar(void)
{
    if (sBarTaskId != TASK_NONE)
    {
        DestroyTask(sBarTaskId);
        SET_BAR_TASK(TASK_NONE);
    }
    if (sBarWindowId != WINDOW_NONE)
    {
        ClearStdWindowAndFrameToTransparent(sBarWindowId, TRUE);
        RemoveWindow(sBarWindowId);
        SET_BAR_WINDOW(WINDOW_NONE);
    }
}

// ---------------------------------------------------------------- specials

void AffinityShowBar(void)
{
    ShowAffinityBar(gSpecialVar_0x8004);
}

void AffinityHideBar(void)
{
    HideAffinityBar();
}

// Applies VAR_0x8005 (signed) to the character in VAR_0x8004 and, if the bar
// for that character is visible, animates it towards the new value.
void AffinityAdd(void)
{
    u32 character = gSpecialVar_0x8004;
    s32 delta = (s16)gSpecialVar_0x8005;
    u32 oldPixels;

    if (character >= AFFINITY_COUNT || delta == 0)
        return;
    oldPixels = AffinityToPixels(GetAffinity(character));
    AddAffinity(character, delta);
    if (sBarWindowId != WINDOW_NONE && sBarCharacter == character)
    {
        if (sBarTaskId != TASK_NONE)
            oldPixels = gTasks[sBarTaskId].tShown;
        StartBarTask(oldPixels, AffinityToPixels(GetAffinity(character)));
    }
}

// Returns the raw affinity (-100..100, as s16 in u16) in VAR_RESULT.
void AffinityGet(void)
{
    gSpecialVar_Result = (u16)(s16)GetAffinity(gSpecialVar_0x8004);
}
