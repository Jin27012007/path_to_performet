#ifndef GUARD_CONSTANTS_LILYCOVE_OPENING_H
#define GUARD_CONSTANTS_LILYCOVE_OPENING_H

// Values of VAR_OPENING_STATE (ordered: scripts compare with >= / <=)
#define OPENING_STATE_NONE        0
#define OPENING_STATE_COMMERCIAL  1  // TV commercial (contest stage, then Lilycove)
#define OPENING_STATE_CABIN       2  // cabin: commercial ends on the monitor
#define OPENING_STATE_CABIN_FREE  3  // exploring the cabin
#define OPENING_STATE_DECK        4  // stepped on deck: crew announcement pending
#define OPENING_STATE_DECK_FREE   5  // on deck, can talk to the crew to disembark
#define OPENING_STATE_ARRIVING    6  // disembarked: port reunion pending
#define OPENING_STATE_HOUSE       7  // entering House 4 with the father (gifts scene)
#define OPENING_STATE_UNPACK      8  // gifts received, go to the spare room
#define OPENING_STATE_ROOM        9  // in the room, bags not stored yet
#define OPENING_STATE_FATHER_LEFT 10 // bags stored; father left while the player was in the room
#define OPENING_STATE_NOTE        11 // back in the living room: read the note on the table
#define OPENING_STATE_FREE        12 // note read: go to the Safari
#define OPENING_STATE_ADOPTED     13 // first Pokémon adopted

#endif // GUARD_CONSTANTS_LILYCOVE_OPENING_H
