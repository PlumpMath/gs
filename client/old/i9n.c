#include "./steam/steam_api.h"
#include <stdio.h>
#include <unistd.h>


//CSteamAPIContext* g_pApiContext = NULL;


extern "C" void api_init()
{

    if (!SteamAPI_Init())
    {
        printf("SteamAPI_Init() failed.");
        return;
    }

    //g_pApiContext = new CSteamAPIContext();

    //if (g_pApiContext == NULL)
    //{
        //printf("new CSteamAPIContext() failed.");
        //return;
    //}

    //if (!g_pApiContext->Init())
    //{
        //printf("CStemApiContext()->Init() failed.");
        //delete g_pApiContext;
        //g_pApiContext = NULL;
        //return;
    //}

    CSteamID steamId = SteamUser()->GetSteamID();

    int friendCount = SteamFriends()->GetFriendCount(k_EFriendFlagImmediate);

    CSteamID friendID;

    for (int i = 0; i < friendCount; i++) {
        friendID = SteamFriends()->GetFriendByIndex(i, k_EFriendFlagImmediate);
        const char *name = SteamFriends()->GetFriendPersonaName(friendID);
        printf(" * %s\n", name);
    }

    //printf("User is logged on: %d.\nFriend count: %d", SteamUser()->BLoggedOn(), friendCount);
}

char ticket[1024];

extern "C" void api_request_ticket() {
    for(int i = 0; i < 1024; i++) {
        ticket[i] = 1;
        printf("%x ", (unsigned char) ticket[i]);
    }
    printf("\n");
    uint32 length;
    HAuthTicket t = SteamUser()->GetAuthSessionTicket(ticket, sizeof(ticket), &length);
    printf("HAuthTicket: %d", t);

    for(int i = 0; i < length; i++) {
        printf("%c ", (unsigned char) ticket[i]);
    }
    printf("\n");
}
