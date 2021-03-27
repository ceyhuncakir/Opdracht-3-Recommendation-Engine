# Recommendation Engine command
Git for the Business rules of the Recommendation Engine.
At the moment the recommendation works on a profile as it can take quite a while before each recommendation can be made

The profile: 5a3e2f8ba82561000176c70a

# Project Members
Ceyhun Cakir | 1784480

# Content Recommendation
Content recommendation is made based on similar categories (main category, gender, target group) of a product

The content recommendation consists of the following steps
```
step 1: Get profile data with the purchased products
step 2: Search for similar products based on categories of the purchased products within the profile
step 3: Add all products with the same categories to a list
step 4: Finally we return 4 random products within the list with the profile ID
```

# Collaborative Recommendation
Collaborative recommendation is made based on similar profiles that have purchased products with the similar categories (main category, gender, target group)

The collaborative recommendation consists of the following steps
```
step 1: Get profile data with the purchased products
step 2: Search for similar profiles based on purchased products with the same categories of the profile where we want to make a recommendation
step 3: Random profile is chosen as a comparable profile
step 4: Randomly chosen products within the randomly chosen profile are added to a list
step 5: Finally we return 4 random products within the list with the profile ID
```

# HUwebshop
As we can see it works on the Huwebshop by looking at the following pictures
![](img/huwebshop-code.png)

![](img/huwebshop-proof.png)
# Version
Versie 1.0.2 | 27-3-2021
