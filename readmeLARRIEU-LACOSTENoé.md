# Micro_language

## Fonctionnalités

### Calcul de base, print

```bash
cmd (type exit(); to leave) > print((2+6)*3);
24
```

### Print d'une chaine de caractère

```bash
cmd (type exit(); to leave) > print("ma jolie string");
ma jolie string
```

### Print concaténation

```bash
cmd (type exit(); to leave) > a = 10;
cmd (type exit(); to leave) > print("a="+a);
a=10

cmd (type exit(); to leave) > print("1+2="+(1+2));
1+2=3
```



### Opérations booléenne

```bash
cmd (type exit(); to leave) > print(3+6 > 9);
False

cmd (type exit(); to leave) > print( (3+6>9) | (2-2==0));
True
```

### Affectation, print

```bash
cmd (type exit(); to leave) > x = 4; x=x+3; print(x);
7
```

### Affectation élargie

```bash
cmd (type exit(); to leave) > x = 4; x++; print(x);
5

cmd (type exit(); to leave) > x = 66; x--; print(x);
65

cmd (type exit(); to leave) > x = 100; x+=3; x-=5; print(x);
98
```

### Condition

```bash
a = 10; 
if a > 9 then { 
	print(a); 
} 
if  a > 10 then {
	printString("never");
}

10
```

### While, For

```bash
cmd (type exit(); to leave) > x=4; while x > 0 { print(x); x--;}
4
3
2
1

cmd (type exit(); to leave) > for (i=0; i < 10; i+=2;) { print(i); }
0
2
4
6
8
```

### Fonction void avec et sans paramètres

```bash
function fibo() {
    n=10;
    first=0;
    second=1;
    while n > 0 {
        tmp=first+second;
        first=second;
        second=tmp;
        print(first);
        n--;
    }
}
fibo();

1
1
2
3
5
8
13
21
34
55

function fibo(n) {
    first=0;
    second=1;
    while n > 0 {
        tmp=first+second;
        first=second;
        second=tmp;
        print(first);
        n--;
    }
}
a=5;
fibo(a);

1
1
2
3
5
```

### Fonction récursive et scope des variables

```bash
function rec(n) {
    if n > 0 then {
        n--;
        rec(n);
        print(n);
    }
}
a=5;
rec(a);
printString("----");
print(a);

0
1
2
3
4
----
5
```

### Retour de fonction

```bash
function factorial(a) {
    if a > 1 then {
        return a * factorial(a-1);
    }
    return a;
}
print(factorial(10));

3628800
```

### Chargement de fichiers de code au démarrage

Possibilité de charger des fichiers au lancement pouvant contenir des déclarations de fonctions ou même des instruction.

**Fichier *fibo* :**

```bash
function fibo(n) {
    first=0;
    second=1;
    while n > 0 {
        tmp=first+second;
        first=second;
        second=tmp;
        print(first);
        n--;
    }
}
```

**Fichier *factorial* :**

```bash
function factorial(a) {
    if a > 1 then {
        return a * factorial(a-1);
    }
    return a;
}
```

**Exécution du programme**

```bash
python main.py fibo factorial

cmd (type exit(); to leave) > fibo(10);

1
1
2
3
5
8
13
21
34
55
```

### Chargement de fichiers de code pendant l'exécution

Possibilité de charger des fichiers pendant l'exécution pouvant contenir des déclarations de fonctions ou même des instruction.

**Fichier *fibo* :**

```bash
function fibo(n) {
    first=0;
    second=1;
    while n > 0 {
        tmp=first+second;
        first=second;
        second=tmp;
        print(first);
        n--;
    }
}
```

**Exécution du programme**

```bash
python main.py

cmd (type exit(); to leave) > load("fibo");
cmd (type exit(); to leave) > fibo(10);

1
1
2
3
5
8
13
21
34
55
```

