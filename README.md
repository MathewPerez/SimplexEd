# SimplexEd
Educational Python library to demonstrate the Simplex Algorithm

## How to Use
Let's say you have the following linear optimization problem:


To put this into the proper canonical form, we first convert it to a maxmization problem by multiplying the objective function by negative one. Then, move the objective function's coefficients to the left hand side, effectively flipping their signs again. 
Now, put the objective function's coefficients into an array. Create a 2-D array, where each row corresponds to the coefficients of a constraint (Note: if a constraint does not involve a certain variable, put a zero as the coefficient at that index). Then, put the right-hand side values of the constraints into an array.
For the above problem, it would look like this:


Then, instantiate an LP object, passing the three arrays as arguments. Use the optimize function and then the decode function to display the solution:


