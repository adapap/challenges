i = 0, a = 1
0   f1()
1   f2: f = 1
2   f5: for f in range(1, b + 1):           ; d = 1
3   f4:     for d in range(1, b + 1):       ; e = d * f
4               if d * f == b:              ; e = 1 if e == b
5                   a += f                  ; i += e
6                                           ; i += 1
7                                           ; a += f
8                                           ; d += 1
9   f3:                                     ; e = 1 if d > b
10                                          ; i += e
11                                          ; f4()
12                                          ; f += 1
13                                          ; e = 1 if f > b
14                                          ; i += e
15                                          ; f5()
16      return a                            ; i *= i
17  f1: b += 2
18      b *= b
19      b *= i
20      b *= 11 ; b = 2 * 2 * 19 * 11 = 836
21      e += 3
22      e *= i
23      e += 7  ; e = 3 * 22 + 7 = 73
24      b += e  ; b = 836 + 73 = 909
25      i += a  ; skip f2
26      f2()
27      e = i
28      e *= i
29      e += i
30      e *= i
31      e *= 14
32      e *= i  ; e = (((((27 * 28) + 29) * 30) * 14) * 32) = 10550400
33      b += e  ; b = 909 + 10550400 = 10551309
34      a = 0
35      f2()