python formatFan.py file.poly

Edit the file getFan to choose between normal or face fan.  Make sure the polytope is centered for face fan.


To create a zonotope in Polymake:

$z=zonotope(new Matrix<Rational>([[0,1,0],[0,0,1]]));
$p=new Polytope<Rational>(POINTS=>$z);
save ($p, "zonotope1.poly");
