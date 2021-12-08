# La vidéo numérique en pratique: Décompression et affichage de flux vidéo

## A - Jouer un flux MPEG-2 élémentaire de test:

1. 

## B - Jouer un flux vidéo de chaîne d’infos américaine assez notoire

1. Le PID du flux vidéo de cnn.ts est 0x1422.

2. `./src/mpeg2dec cnn.ts -o pgm -v -t 0x1422`
