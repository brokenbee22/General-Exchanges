general exchange

this is a website i made for buying and selling raw materials online. the idea is basically like if amazon or ebay was more focused on stuff like wood, steel, bricks, cement, pvc, gravel, and other construction materials. right now it is still in beta and it is more like a working version to show the idea, not something fully finished yet.

the project was made with python and django. i used django because it already has a lot of the backend stuff ready like users, admin panel, database models, forms, and routing, so it made more sense for this type of marketplace project. the frontend is mostly html and css with django templates. i tried to keep it simple but still make it look like an actual website and not just a plain school project.

the website lets sellers register, but they do not automatically get approved. the admin has to approve them first before their products show up on the marketplace. this was added because if this was a real website, i would not want random sellers posting fake listings or bad products. after the seller gets approved, they can add products and those products can show up on the main page.

buyers can browse products, search by name, filter by category, and add items to the cart. the cart works using sessions, so the user does not need an account just to test the buying flow. there is also a checkout page, but it is still a test checkout, so it creates an order but does not charge a real payment yet. payments would probably be added later with something like stripe.

the website also has a basic seller dashboard. sellers can see their products and the orders they got. there is also a marketplace fee idea where general exchange takes 5 percent from the seller side. the buyer does not see that fee because it is supposed to work more like ebay, where the seller price is shown to the buyer and the platform fee is deducted from the seller payout.

i also added demo products like steel and wood so the site does not look empty. the images are stored in the static folder for now because this is just a beta version. later, if this became more serious, product images should probably use something like cloudinary or amazon s3 instead of local files.

this project helped me practice django, python backend logic, templates, static files, user authentication, admin approval, carts, checkout flow, product listings, and deployment. it is not perfect yet, but the main idea works and it is a good starting point for a raw materials marketplace.