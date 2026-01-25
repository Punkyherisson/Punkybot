<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Est ce que l'on peut avoir plusieurs bots qui tournent en meme temps sur le serveur discord ?

Oui, tu peux avoir plusieurs bots différents qui tournent en même temps sur le même serveur Discord.[^5][^6]

### Ce qui est possible

- Tu peux ajouter autant de bots que tu veux (MEE6, Dyno, un bot maison, etc.) tant que ton serveur les accepte et qu’ils respectent les règles de Discord.[^6][^5]
- Chaque bot est une application distincte avec son propre token, ses propres permissions et son propre « profil » sur le serveur.[^1][^4]
- Ils peuvent tous écouter les mêmes messages, chacun décidera s’il doit réagir ou non en fonction de son préfixe, de ses slash commands, etc.[^2][^5]


### Points d’attention

- Conflits de commandes : éviter que deux bots utilisent exactement le même préfixe et les mêmes noms de commandes (`!play`, `!help`, etc.), sinon ça devient vite le bazar.[^5]
- Ressources : plus tu as de bots, plus ça génère de messages, de logs et de requêtes d’API, donc sur un gros serveur ça peut peser un peu.[^5]
- Lisibilité : trop de bots peut perdre les membres, donc en pratique on limite souvent à 2–5 bots bien choisis plutôt que 15 petits bots.[^6][^5]


### Ce qui n’est pas possible

- Tu ne peux pas ajouter *exactement* le même bot (même application/token) deux fois sur le même serveur : un bot donné ne peut être présent qu’une seule fois sur un serveur, même si tu le fais tourner sur plusieurs instances de code.[^4][^1][^2]

Si tu veux, dis-moi ce que tu imagines comme combinaison (par ex. bot maison + modération + musique) et je peux te suggérer une architecture “propre” pour ton serveur.
<span style="display:none">[^10][^3][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://www.reddit.com/r/discordbots/comments/16wyt1t/two_instances_of_1_bot_in_same_server/

[^2]: https://www.reddit.com/r/discordapp/comments/9an1zk/is_there_a_way_to_have_multiple_of_the_same_bot/

[^3]: https://www.youtube.com/watch?v=qfUoPTZmlM0

[^4]: https://www.reddit.com/r/Discord_Bots/comments/bkp0zl/connect_multiple_applications_to_one_bot/

[^5]: https://www.bot-discord.click/peut-on-installer-plusieurs-bots/

[^6]: https://www.dropingame.com/blog/index.php/2019/11/18/trouver-inviter-et-configurer-un-bot-discord-sur-son-serveur/

[^7]: https://www.youtube.com/watch?v=A5cWnjWCoOE

[^8]: https://www.reddit.com/r/discordapp/comments/1jxuvmy/how_do_i_add_multiple_music_bots_to_discord/

[^9]: https://www.draftbot.fr/premium

[^10]: https://www.elephorm.com/formation/bureautique/creer-et-administrer-un-serveur-discord/utilisation-et-configuration-des-bots-sur-discord

