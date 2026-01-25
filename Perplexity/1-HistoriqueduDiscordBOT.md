<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# ok je suis en train de regarder car j'avais fait un bot discord il y a longtemps et je ne m'en souvenais plus ... je suis ici comment je fais pour avoir le token de mon bot ?

[My Applications | Discord Developer Portal](https://discord.com/developers/applications/1341902375220281346/information)

Oui, tu peux récupérer (ou plutôt régénérer) le token de ton bot depuis cette page, mais Discord ne montre plus l’ancien token : il faut en créer un nouveau.[^1]

## Où cliquer dans le Developer Portal

1. Sur la page de ton application (le lien que tu as envoyé), regarde le menu à gauche.
2. Clique sur l’onglet **Bot** (icône pièce de puzzle).[^2]

Tu devrais arriver sur une page avec ta section **Build-A-Bot**, l’avatar du bot, puis la partie **Token**.

## Récupérer / recréer le token

- Sous la section **Token**, tu n’auras plus un bouton « Reveal », mais un bouton **Reset Token**.[^3][^1]
- Clique sur **Reset Token**, confirme (et entre ton code 2FA si demandé).
- Discord affiche alors un **nouveau token une seule fois**, avec un bouton **Copy** : copie-le tout de suite et colle-le dans ton `.env`, variables Replit, etc.[^4][^5]

Important :

- L’ancien token devient immédiatement invalide dès que tu fais « Reset Token » ; mets bien le nouveau dans ton code avant de relancer le bot.[^6]
- Ne partage jamais ce token, ni en capture, ni dans GitHub (utilise des variables d’environnement dans Replit).[^7]

Si tu veux, tu peux coller ton code de démarrage du bot (en cachant le token) et il sera adapté pour utiliser une variable d’environnement sur Replit.
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://support-dev.discord.com/hc/en-us/articles/6470840524311-Why-can-t-I-copy-my-bot-s-token

[^2]: https://github.com/reactiflux/discord-irc/wiki/creating-a-discord-bot-\&-getting-a-token

[^3]: https://support-dev.discord.com/hc/fr/articles/6470840524311-Pourquoi-est-ce-que-je-ne-peux-pas-copier-le-token-de-mon-bot

[^4]: https://iproyal.com/blog/python-discord-api-guide/

[^5]: https://discord.com/developers/docs/quick-start/getting-started

[^6]: https://discordjs.guide/legacy/preparations/app-setup

[^7]: https://doc.crowbots.shop/token

[^8]: https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/101966486/855272c0-c8fa-4b54-984b-a10e599a4945/image.jpg

[^9]: https://www.youtube.com/watch?v=5SRwnLYdpJs

[^10]: https://www.youtube.com/watch?v=cKF6X5OuxQQ\&vl=fr

[^11]: https://cybrancee.com/blog/how-to-make-a-simple-discord-bot-ultimate-2025-guide/

[^12]: https://stackoverflow.com/questions/71461736/why-there-is-no-reveal-token-when-i-making-discord-bot

[^13]: https://www.writebots.com/discord-bot-token/

[^14]: https://www.youtube.com/watch?v=6XAZknOFQms

[^15]: https://lmno.pk/post/discord-bot-token/

[^16]: https://www.youtube.com/watch?v=DwvJc-pLYFY

[^17]: https://docs.aethex.tech/docs/discord-bot-token-fix

[^18]: https://discord.com/developers/docs/reference

[^19]: https://www.tokenmetrics.com/blog/mastering-discord-integrations-api-essentials?0fad35da_page=34\&617b332e_page=25\&74e29fd5_page=8

[^20]: https://cybrancee.com/learn/knowledge-base/how-to-reset-your-discord-bot-token/

[^21]: https://allaboutcookies.org/discord-bot-hosting-guide

