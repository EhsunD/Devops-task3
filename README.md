# Devops-task3
This tasks is about programming and Docker compose.

# Step1:
Write a simple Microservice with 3 services: 1. Accounts 2. Shop 3. Order

Accounts:

1. Login -> username, password => token .
2. Signup -> username, password .
3. Logout -> delete token .
4. CheckToken -> token => user .

Shop:

1. Add to Cart .
2. Get Items
3. Item Detail
4. Remove from Cart .
5. Add Order -> Finalize Cart
6. Pay Order

Order:

1. AddOrder
2. GetOrders
3. GetOrderDetail

# Step2:
Dockerize all microservices and Deploy them with docker-compose.

# Step3:
Deploy an nginx with 3 replicas and an HAProxy that load balances between these 3 replicas.

Nginx routes should be like the below:

**domain.com/accounts -> accounts_microservice**

**domain.com/shop -> shop_microservice**

**domain.com/order -> order_microservice**

### Network Schematic:

**Client -> HAProxy -> nginx1, nginx2, nginx3 -> microservices**

# Step4:
Enable rate limiting on nginx based on user IP.

More on nginx rate limiting (You must read this document): **https://www.nginx.com/blog/rate-limiting-nginx/**
