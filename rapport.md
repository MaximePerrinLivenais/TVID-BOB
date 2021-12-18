# La vidéo numérique en pratique: Décompression et affichage de flux vidéo

## A - Jouer un flux MPEG-2 élémentaire de test:

1. Nous avons choisi d'expérimenter notre désentrelaceur sur pendulum.m2v et
    numbers_bw.m2v

2. Done

3. On peut remarquer que l'image est composé des 3 canaux YUV. En effet sur
    les 2/3 supérieurs de l'image on peut retrouver la luminance. On peut
    ensuite remarquer dans le dernier tier du ppm les 2 canaux UV, tous les
    2 samplés en 4:2:0.

4. Done.

5. Done

6. Done

7. Done

8. Done

9. Done

10. Done

## B - Jouer un flux vidéo de chaîne d’infos américaine assez notoire

1. Le PID du flux vidéo de cnn.ts est 0x1422.

2. `./src/mpeg2dec cnn.ts -o pgm -v -t 0x1422`

3. Le flux video semble osciller de haut en bas puis de bas en haut de maniere
    periodique.

4. A voir

5. A faire

6. Je sais aps

## C - Jouer un flux vidéo de chaînes de divertissement asiatiques

1. Le troisieme PID vidéo de ctv.ts est 0x3fd.

2. Done

3. Nous avons pu remarquer une différence de vitesse entre les effets spéciaux
    et le reste de la scène. Ce qui nous a permis de voir cette différence est
    le moment où la petite fille décide de prendre sa fourchette en main le
    mouvement se saccade. Nous avons donc l'impression que pour pouvoir garder
    des effets spéciaux qui seraient pas trop rapide, certaines images ont été
    déboublés pour que le nombre de frames d'effets spéciaux soit égal à celle
    de la scène originale.

4. Le premier PID vidéo de ctv.ts est 0x3e9.

5. Done

6. Meme apres desentrelacement certains moments du flux semblent encore entrelaces.
    Ceci etait deja observable dans la video precedente au moment ou le pere pose
    le gateau mais c'est desormais tres marque.

## D - Vers un meilleur désentrelaceur

1. Done reste selection du seuil

2. Mollot l'asticot

3. J'ai dit mollot le poto
