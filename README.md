# TriangleGame
Add The Numbers In All Possible Sub-Triangular Regions of a Graph

http://www.grant-trebbin.com/2016/01/find-all-triangles-in-diagram-and-add.html

http://www.grant-trebbin.com/2016/01/merging-regions-defined-by-list-of.html

A recent TV game show piqued my interest and I wasn't satisfied until I found a systematic way to solve it.  The way to programatically solve the game is descirbed in the blog posts linked at the top of the page.  This is just an explanantion of how to use the software for example shown below.

![](https://github.com/GrantTrebbin/TriangleGame/blob/master/20151215_214417.jpg)

If we focus on just the puzzle we can see that the people that design it try to trick you by using using Roman numerals.  It's not visible in this puzzle, but sometimes it also looks like lines meet and create a vertex when they actually don't.

![](https://github.com/GrantTrebbin/TriangleGame/blob/master/20151215_214417s.png)

The first step is to remove all that's irrelevant, restating the problem in a simpler way.  First all the vertices are labeled, then all the regions are labeled with their corresponding values.  In the image below it can be seen that the vertices 1, 2, and 8 create the region 3 which has a value of 5.

![](https://github.com/GrantTrebbin/TriangleGame/blob/master/drawing1.png)

asdf

asdf
```python
regions_1 = {Region({1},  8, [2,  3,  9]),
             Region({2},  3, [9,  3,  4]),
             Region({3},  5, [1,  2,  8]),
             Region({4},  2, [2,  9, 10, 8]),
             Region({5},  4, [9,  4, 10]),
             Region({6},  8, [1,  8,  7]),
             Region({7}, 10, [8, 10,  6, 7]),
             Region({8},  1, [6, 10,  4]),
             Region({9},  9, [6,  4,  5])}

straight_lines_1 = [StraightLineSegment({1, 2, 3}),
                    StraightLineSegment({1, 8, 10, 4}),
                    StraightLineSegment({1, 7, 6, 5}),
                    StraightLineSegment({2, 8, 7}),
                    StraightLineSegment({3, 9, 10, 6}),
                    StraightLineSegment({2, 9, 4}),
                    StraightLineSegment({3, 4, 5})]

triangle_game_1 = StructuredNetwork(regions_1, straight_lines_1)
```

```
Triangular Regions ({id} =value= *vertices*)
count = 22

({8, 6, 7} =19= *7* *1* *8* *10* *4* *6*)
({3, 6} =13= *1* *2* *8* *7*)
({1, 2} =11= *2* *3* *4* *9*)
({6, 7} =18= *10* *6* *7* *1* *8*)
({1, 2, 3, 4, 5} =22= *2* *3* *4* *10* *8* *1*)
({5} =4= *9* *4* *10*)
({3} =5= *1* *2* *8*)
({8, 9, 6, 7} =28= *5* *6* *7* *1* *8* *10* *4*)
({2, 5} =7= *4* *10* *9* *3*)
({9} =9= *5* *6* *4*)
({2} =3= *4* *9* *3*)
({8, 9, 2, 5} =17= *4* *5* *6* *10* *9* *3*)
({1, 2, 3, 4, 5, 6, 7, 8, 9} =50= *1* *2* *3* *4* *5* *6* *7*)
({1, 3, 4, 6, 7} =33= *7* *1* *2* *3* *9* *10* *6*)
({8} =1= *6* *10* *4*)
({1, 3, 4} =15= *2* *3* *9* *10* *8* *1*)
({8, 5} =5= *9* *4* *6* *10*)
({8, 2, 5} =8= *4* *6* *10* *9* *3*)
({3, 4, 5} =11= *8* *1* *2* *9* *4* *10*)
({6} =8= *1* *8* *7*)
({1} =8= *2* *3* *9*)
({4, 5} =6= *4* *10* *8* *2* *9*)


Sum of all the numbers in each triangular region = 301
```
