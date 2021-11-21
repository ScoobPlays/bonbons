# applications = {
#     "poker": disnake.PartyType.poker,
#     "betrayal": disnake.PartyType.betrayal,
#     "fishing": disnake.PartyType.fishing,
#     "chess": disnake.PartyType.chess,
#     "lettertile": disnake.PartyType.letter_tile,
#     "wordsnack": disnake.PartyType.word_snack,
#     "doodle_crew": disnake.PartyType.doodle_crew,
#     "checkers": disnake.PartyType.checkers,
#     "spellcast": disnake.PartyType.spellcast,
#     "awkword": disnake.PartyType.awkword,
#     "sketchy_artist": disnake.PartyType.sketchy_artist,
#     "putt_party": disnake.PartyType.putt_party,
#     "youtube": disnake.PartyType.watch_together,
# }

# async def start_activity(ctx, name: str):
#     await ctx.send(await ctx.author.voice.channel.create_invite(target_application=applications[name], target_type=disnake.InviteTarget.embedded_application))