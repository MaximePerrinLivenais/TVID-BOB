# La vidéo numérique en pratique: Décompression et affichage de flux vidéo

## A - Jouer un flux MPEG-2 élémentaire de test:

1. Nous avons choisi d'expérimenter notre désentrelaceur sur pendulum.m2v et
    numbers_bw.m2v

2. Done

3. On peut remarquer que l'image est composé des 3 canaux YUV. En effet sur
    les 2/3 supérieurs de l'image on peut retrouver la luminance. On peut
    ensuite remarquer dans le dernier tier du ppm les 2 canaux UV, tous les
    2 samplés en 4:2:0.

4. Check comment on fait.

5. Done

6. Done

7. Done

8. Check comment on fait

9. Pipe frame period dans le desentrelaceur

10. Pipe les caracs de chaque frame dans le desentrelaceur

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

3. Sa mère j'arrive pas à voir la diff.

4. Le premier PID vidéo de ctv.ts est 0x3e9.

5. Done

6. Sa mère j'arrive pas à voir la diff.

## D - Vers un meilleur désentrelaceur


