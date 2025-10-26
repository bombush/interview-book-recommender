book_readers = dataset_lowercase['User-ID'][dataset_lowercase['ISBN'] == book_isbn.lower()]

    #book_readers = dataset_lowercase['User-ID'][(dataset_lowercase['Book-Title'] == target_book_title)& (dataset_lowercase['Book-Author'] == target_book['Book-Author'].values[0].lower())]
    #book_readers = dataset_lowercase['User-ID'][(dataset_lowercase['Book-Title']=='the fellowship of the ring (the lord of the rings, part 1)') & (dataset_lowercase['Book-Author'].str.contains("tolkien"))]



author lowercase

Books similar to 'The Fellowship of the Ring (The Lord of the Rings, Part 1)':
                                                 book      corr  Book-Rating
0                                   a wrinkle in time  0.966877     8.222222
12  the drawing of the three (the dark tower, book 2)  0.908581     8.500000
9                                        pet sematary  0.891457     7.600000
15                the hobbit: or there and back again  0.848986     8.666667
13            the gunslinger (the dark tower, book 1)  0.762539     8.285714
14               the hitchhiker's guide to the galaxy  0.751265     7.625000
21                                     watership down  0.745533     8.125000
2                                        dreamcatcher  0.711490     6.611111
17  the return of the king (the lord of the rings,...  0.633280     9.531250
10                                           stardust  0.581318     7.888889


book tolkien

Books similar to 'The Fellowship of the Ring (The Lord of the Rings, Part 1)':
                                                 book      corr  avg_rating
33                                           stardust  0.909450    7.541667
38  the drawing of the three (the dark tower, book 2)  0.907758    8.818182
53                              the phantom tollbooth  0.896262    8.111111
24                                                 it  0.887229    8.363636
66                                      the testament  0.852803    8.333333
4                                   a wrinkle in time  0.848478    8.333333
9       ender's game (ender wiggins saga (paperback))  0.836660    9.333333
29                                       pet sematary  0.830264    8.250000
47                the hobbit: or there and back again  0.820499    8.800000
40                                           the gift  0.808511    7.300000


original script

33                                           stardust  0.909450    7.500000
38  the drawing of the three (the dark tower, book 2)  0.907758    8.000000
53                              the phantom tollbooth  0.896262    8.500000
24                                                 it  0.887229    8.333333
66                                      the testament  0.852803    8.000000
4                                   a wrinkle in time  0.848478    8.357143
9       ender's game (ender wiggins saga (paperback))  0.836660    9.307692
29                                       pet sematary  0.830264    7.636364
47                the hobbit: or there and back again  0.820499    8.800000
40                                           the gift  0.808511    7.750000

grouped by ISBN
Books similar to 'The Fellowship of the Ring (The Lord of the Rings, Part 1)':
                                                book      corr  avg_rating
7                the hobbit: or there and back again  0.848986    8.666667
1   harry potter and the chamber of secrets (book 2)  0.389387    8.444444
5     harry potter and the sorcerer's stone (book 1)  0.280583    8.818182
9     the two towers (the lord of the rings, part 2)  0.266481    9.708333
8  the return of the king (the lord of the rings,...  0.159642    9.727273
6               the hitchhiker's guide to the galaxy  0.157378    8.428571
4  harry potter and the prisoner of azkaban (book 3) -0.053343    9.136364
2       harry potter and the goblet of fire (book 4) -0.308395    9.375000
3  harry potter and the order of the phoenix (boo... -0.540226    9.125000
0                              bridget jones's diary -0.553050    7.666667