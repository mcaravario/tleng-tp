a = true;
b = false;
c = a AND b;
d = NOT false;
e = d OR false;
f = c == b;
g = (a != c);
x = 5;
y = 10;
h = (e AND false) OR ((x < 1) == (y > 2));
i = NOT f ? (x > 5 ? y : 10) : x + 5;
j = [true, false];
k = [1, 2, 3];
l = j[1] ? (k[1] == k[3]) : j[2] == a ? b : c;
m = ((x + k[2] > 3) ? 2 ^ k[0] : (j[2] ? k[1] + 6 : (y)));
