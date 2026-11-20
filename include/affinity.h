#ifndef GUARD_AFFINITY_H
#define GUARD_AFFINITY_H

s32 GetAffinity(u32 character);
void SetAffinity(u32 character, s32 value);
void AddAffinity(u32 character, s32 delta);
void ShowAffinityBar(u32 character);
void HideAffinityBar(void);

#endif // GUARD_AFFINITY_H
