// Minimal headless GBA runner for testing the hack's scenes.
// Usage: gbarun rom.gba script.txt outdir
// Script commands (one per line):
//   wait N            run N frames with no keys
//   press KEYS N      hold KEYS (e.g. A, UP, A+B) for N frames, then release 1 frame
//   tap KEYS [times]  press KEYS for 4 frames + 12 frames idle, repeated
//   shot NAME         save screenshot NAME.ppm into outdir
//   savestate NAME / loadstate NAME   (in outdir)
#include <mgba/core/core.h>
#include <mgba/core/serialize.h>
#include <mgba-util/vfs.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static struct mCore *core;
static color_t *buf;
static unsigned W, H;
static char outdir[512];

static uint32_t parseKeys(const char *s)
{
    static const char *names[] = {"A","B","SELECT","START","RIGHT","LEFT","UP","DOWN","R","L"};
    uint32_t k = 0; char tmp[128]; strncpy(tmp, s, 127); tmp[127] = 0;
    for (char *t = strtok(tmp, "+"); t; t = strtok(NULL, "+"))
        for (int i = 0; i < 10; i++) if (!strcmp(t, names[i])) k |= 1u << i;
    return k;
}
static void frames(uint32_t keys, int n) { core->setKeys(core, keys); for (int i = 0; i < n; i++) core->runFrame(core); }
static void shot(const char *name)
{
    char p[1024]; snprintf(p, sizeof p, "%s/%s.ppm", outdir, name);
    FILE *f = fopen(p, "wb"); fprintf(f, "P6\n%u %u\n255\n", W, H);
    for (unsigned i = 0; i < W * H; i++) { uint32_t c = buf[i]; unsigned char px[3] = {c & 0xFF, (c >> 8) & 0xFF, (c >> 16) & 0xFF}; fwrite(px, 1, 3, f); }
    fclose(f);
}
int main(int argc, char **argv)
{
    if (argc < 4) return 1;
    strncpy(outdir, argv[3], 511);
    core = mCoreFind(argv[1]);
    if (!core || !core->init(core)) { fprintf(stderr, "core\n"); return 1; }
    mCoreInitConfig(core, NULL);
    core->desiredVideoDimensions(core, &W, &H);
    buf = calloc(W * H, sizeof(color_t));
    core->setVideoBuffer(core, buf, W);
    if (!mCoreLoadFile(core, argv[1])) { fprintf(stderr, "rom\n"); return 1; }
    // Fixed clock (midday) so runs are deterministic and the overworld is not tinted for night.
    core->rtc.override = RTC_FIXED;
    core->rtc.value = 1781524800000LL;
    core->reset(core);
    FILE *sf = fopen(argv[2], "r"); char line[256];
    while (fgets(line, sizeof line, sf)) {
        char cmd[32] = {0}, a[128] = {0}; int n = 0;
        int c = sscanf(line, "%31s %127s %d", cmd, a, &n);
        if (c < 1 || cmd[0] == '#') continue;
        if (!strcmp(cmd, "wait")) frames(0, atoi(a));
        else if (!strcmp(cmd, "press")) { frames(parseKeys(a), n > 0 ? n : 4); frames(0, 1); }
        else if (!strcmp(cmd, "tap")) { int t = n > 0 ? n : 1; for (int i = 0; i < t; i++) { frames(parseKeys(a), 4); frames(0, 12); } }
        else if (!strcmp(cmd, "shot")) shot(a);
        else if (!strcmp(cmd, "savestate")) { char p[1024]; snprintf(p, sizeof p, "%s/%s.ss", outdir, a); struct VFile *vf = VFileOpen(p, O_CREAT | O_TRUNC | O_RDWR); mCoreSaveStateNamed(core, vf, SAVESTATE_ALL); vf->close(vf); }
        else if (!strcmp(cmd, "loadstate")) { char p[1024]; snprintf(p, sizeof p, "%s/%s.ss", outdir, a); struct VFile *vf = VFileOpen(p, O_RDONLY); mCoreLoadStateNamed(core, vf, SAVESTATE_ALL); vf->close(vf); }
    }
    core->deinit(core);
    return 0;
}
