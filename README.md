# Computational_Planning
Motion Planning based on Computational Geometry 

## Brehemnsan Algorithm 
The approach focuses on finding or clustering the obstacles in our direction. We do this by the vector projection concept. This works as a directional filter which projects the obstacles on our direction of approach by computing how much of each obstacle's relative position to the current position is in the direction of movement. It is crucial that the projection must not only be positive but also in the actual direction of the vector to ensure the obstacle is ahead and not behind.

Once, the obstacles that lie in our direction is taken care we move forward to find the obstacle that is closest to us. 
[Doc](https://docs.google.com/document/d/1HwhR370o9kS2Lb4gRbg8JsDy_vtT5b6vlm_0Y4IKhEk/edit)

## Results 
![Circle with closest distance as radius](brehemnsan.png)

![Obstacles Exploration](obstacles.png)
