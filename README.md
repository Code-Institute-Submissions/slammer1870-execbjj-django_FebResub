# ExecBJJ Website
![image](https://user-images.githubusercontent.com/42610577/133406469-cfa248d1-02d7-4d19-b337-c19859cc5578.png)
[ExecBJJ - View The Live Deployed Website](https://execbjj-django-preprod.herokuapp.com/)

*This is software that is actively used in production, linked above the the preproduction environment. Please see the pre-production branch for project code

# Table of Contents
- [ExecBJJ Website](#execbjj-website)
- [Table of Contents](#table-of-contents)
  * [Author](#author)
  * [Project Overview](#project-overview)
  * [HOW TO USE](#how-to-use)
    + [Unauthenticated User](#unauthenticated-user)
    + [Standard User](#standard-user)
    + [Admin User](#admin-user)
  * [UX](#ux)
    + [Strategy](#strategy)
    + [Project Goals](#project-goals)
      - [User Goals](#user-goals)
      - [Developer Goals](#developer-goals)
      - [Website Owner Goals](#website-owner-goals)
    + [User Stories](#user-stories)
    + [Design Choices](#design-choices)
      - [Colors](#colors)
      - [Typography](#typography)
      - [Images](#images)
      - [Design Elements](#design-elements)
      - [Custom Javascript](#custom-javascript)
    + [Wireframes](#wireframes)
    + [Features](#features)
      - [Future Features](#future-features)
- [Information Architecture](#information-architecture)
  * [Database Choice](#database-choice)
    + [Data Models](#data-models)
- [Technologies Used](#technologies-used)
  * [Programming Languages](#programming-languages)
  * [Fonts](#fonts)
  * [Tools](#tools)
  * [APIs](#apis)
- [Defensive Programming](#defensive-programming)
    + [Access Controls](#access-controls)
    + [Permission Roles](#permission-roles)
  * [Testing](#testing)
    + [Penetration Testing](#penetration-testing)
      - [Testing Authenticated Routes](#testing-authenticated-routes)
      - [Result](#result)
      - [Testing Role Based Permissions](#testing-role-based-permissions)
      - [Result](#result-1)
    + [Validation Testing](#validation-testing)
    + [Cross Browser and Cross Device Testing](#cross-browser-and-cross-device-testing)
    + [Automated Testing](#automated-testing)
    + [Manual Testing](#manual-testing)
      - [1. Newsletter form:](#1-newsletter-form-)
        * [Results](#results)
      - [2. Contact form:](#2-contact-form-)
        * [Results](#results-1)
      - [3. Registration Page:](#3-registration-page-)
        * [Results](#results-2)
      - [4. Login Page:](#4-login-page-)
        * [Results](#results-3)
      - [5. Dashboard Page:](#5-dashboard-page-)
        * [Results](#results-4)
      - [6. Post Edit Functionality:](#6-post-edit-functionality-)
        * [Results](#results-5)
      - [7. Post Delete Functionality:](#7-post-delete-functionality-)
        * [Results](#results-6)
      - [8. Logout Functionality:](#8-logout-functionality-)
        * [Results](#results-7)
      - [9. Conditional Rendering:](#9-conditional-rendering-)
        * [Results](#results-8)
    + [Defect Tracking](#defect-tracking)
    + [Defects of Note](#defects-of-note)
  * [Deployment](#deployment)
    + [Deploy Locally](#deploy-locally)
    + [Deploy To Heroku](#deploy-to-heroku)
  * [Credits](#credits)
    + [Content](#content)
    + [Media](#media)
    + [Acknowledgments](#acknowledgments)

## Author
Sam Mc Nally


## Project Overview
This site is design with a landing page for lead capturing and studio infomration as well as a dashboard for authenticated users. Users can create an account, login, manage their subscriptions, check in for classes, cancel their appointments as well as being able to sign up for newsletter updates and sumbit queries through a contact form. 

## HOW TO USE
To use this website the steps are as follows.

- Step 1: Login users login by navigating to the "/login" route, if user does not have an account they can login by clicking the "Click here to register" link on the login form.\
![image](https://user-images.githubusercontent.com/42610577/146531896-2c890de6-d19e-4312-94c9-85fb1a3fb1e6.png)- Step 2: Once logged in a user will be redirected to the dashboard.\
![image](https://user-images.githubusercontent.com/42610577/146532342-f9fd4d38-387f-4972-a860-9f4d64ce5855.png)- Step 3: Users can manage their memberships from here, view the technique of the week as well as check into classes.\
![image](https://user-images.githubusercontent.com/42610577/146532528-c0341553-b797-4175-b1dc-d504de63a1d0.png)

### Unauthenticated User
Unauthenticated Users can access the landing page, login page and registration page. The site is built with access controls to stop unauthenticated users from accessing the dashboard.

### Standard User
- A standard user can manage their own membership including creating, updating, deleing and check in to classes/cancel their bookings.

### Admin User
- Currently there is no permission restricted only to admin users via the interface of the website. Admin controls are managed through the Django admin dashboard.

## UX
As this is a CRUD based application the key UX features for this site are clear and defined input for accessability. Examples of this can be seen on the chck in and cancel buttons for bookings.\
![image](https://user-images.githubusercontent.com/42610577/146533066-636dc623-e826-4723-9759-23051af327d5.png)

### Strategy
The strategy behind this website is to use of for a company that I own that is in the process of opening back up after being shut for over a year.

### Project Goals
The goal of this project is to deliver a simple, user friendly and intuitive application that allows user to create and manage subscriptions and check into classes

#### User Goals
As a user I want to have a clear and intuitive experience through out the application with consisten visual feedback in the form of flashed messages as I interact with the website.

#### Developer Goals
As a developer I aim to produce an CRUD application with User Authentication as well as a defensive programming design strategy to ensure that user's data is protected.

#### Website Owner Goals
As a product owner I aim to have a piece of software that is built with clean foundational architecture that provides for the ability to add more directly monetisable features like premium membership content and payment integrations into the site.


### User Stories
As a User I want to be able to sign up to a newsletter, submit queries via a contact form, create an account, login, manage my mebership and check into classes.


### Design Choices
The most prominent design choices in this application are to be found in the visual feedback of the alert messages with Green being used for success messages, Yellow for standard operations like post editing and Red for error messages.

As well as this providing users with their own data aggregated into the "My Posts" section is design to that users can access their posts directly from the message board and have the posts that they own filtered in the "My Posts" section.

#### Colors
The colours used in this project are simple Greys and Black for structual elements of the pages, Red and Blue for the edit and delete button and Green, Yellow and Red for visual feedback in the alert messages depening on the nature of the interaction.

#### Typography
The typography used is Montserrat. Montserrat has a clean layout and fits the theme of this site well.

#### Images
The images used are all relating to the activities of the company. They are mostly high quality JPEGs.

#### Design Elements

Forms.\
![image](https://user-images.githubusercontent.com/42610577/146533821-2edeeee5-401d-46d2-9d06-78e97e7af6b8.png)

Input Buttons.\
![image](https://user-images.githubusercontent.com/42610577/146533066-636dc623-e826-4723-9759-23051af327d5.png)

Cards.\
![image](https://user-images.githubusercontent.com/42610577/146533923-bf27f8d6-9a1f-4272-857c-1c51d12c67fb.png)

#### Custom Javascript
There is a timeout function on the alert messages so that the dissapear after 5 seconds.
``` 
<script>
  window.setTimeout(
    "document.getElementById('alert').style.display='none';",
    5000
  );
</script>
 ```

### Wireframes

I built full mobile and desktop mockups using Adobe XD.\
![image](https://user-images.githubusercontent.com/42610577/146534177-d4410e02-7792-4337-b6ab-243eead89f1f.png)

### Features
Lead capture form.\
![image](https://user-images.githubusercontent.com/42610577/133422290-92cba907-24b7-4200-9edd-c9c18f378f0d.png)

Contact form.\
![image](https://user-images.githubusercontent.com/42610577/133422362-b50e0daa-b446-4a27-8de2-2aed01a22fe3.png)

Login page.\
![image](https://user-images.githubusercontent.com/42610577/133422473-d04628b3-b5da-4d6d-8f0c-4e6f5d384c04.png)

Registration page.\
![image](https://user-images.githubusercontent.com/42610577/133422519-a8c4ce11-0085-4230-8c24-cd24d763f13f.png)

Dashboard.\
![image](https://user-images.githubusercontent.com/42610577/146532342-f9fd4d38-387f-4972-a860-9f4d64ce5855.png)


# Information Architecture

The functionality of the application is very simple. When a user signs up they are assigned a Stripe customer id via a Django signal.

```
# Receiver to create customer in Stripe and assing their StripeID to the CustomUser object


@receiver(post_save, sender=CustomUser)
def create_stripe_id(sender, instance, **kwargs):

    name = str("{0} {1}").format(instance.first_name, instance.last_name)

    if instance.stripe_customer_id == None:

        stripe_customer = stripe.Customer.create(
            name=name,
            email=instance.email
        )

        instance.stripe_customer_id = stripe_customer["id"]

        post_save.disconnect(create_stripe_id, sender=CustomUser)
        instance.save()
        post_save.connect(create_stripe_id, sender=CustomUser)
```

This Stripe ID is then used for all user interactions with Stripe. A Stripe product ID is assigned to each product that is then used to reference in Stripe.

The business logic for completed payments are handled in the payment success view, this view can handle both individual product purchases as well as subscriptions

```
@login_required
def success_view(request):

    # Gets sessionID from URL parameters
    session_id = request.GET.get("session_id")

    # Gets line item from checkout session
    line_item = stripe.checkout.Session.list_line_items(session_id, limit=1)

    # Retrieves checkout session object
    checkout_session = stripe.checkout.Session.retrieve(session_id)

    if checkout_session['subscription']:
        sub_id = checkout_session['subscription']
    else:
        sub_id = ""

    # Creates new subscription with request user, priceID from line item (only works with one line item), subscriptionID from checkout session and sets status to active
    subscription, created = Subscription.objects.update_or_create(user=request.user, defaults={'membership': Membership.objects.get(
        stripe_price_id=line_item.data[0].price.id), 'stripe_subscription_id': sub_id, 'status': "active"})
    subscription.save()

    messages.success(request, "Thank for you subscribing!")

    return redirect('dashboard_redirect')

```

Updating and deleting subscriptions is handled by a webhook that is sent to the "/webhook" endpoint.

Check ins verify that the user has an active subscription before allowing the function to execute.

## Database Choice
Postgres

### Data Models
![image](https://user-images.githubusercontent.com/42610577/146538482-3c5893ae-0862-480d-999d-971e8f85c8f0.png)


# Technologies Used

- A variety of different technologies were user:
  - [Tailwind CSS](https://tailwindcss.com/) - A utility first CSS Framework
  - [Alpine JS](https://alpinejs.dev/) - A lightweight Javascript Framework
  - [Mailchimp](https://mailchimp.com/) - An email marketing platform
  - [Sendgrid](https://sendgrid.com/) - An email delivery API
  - [Stripe](https://stripe.com/) - Payments Integration Software
  

## Programming Languages

- [CSS3](https://www.w3schools.com/w3css/default.asp) - used to style DOM appearance. 
- [HTML5](https://www.w3schools.com/html/default.asp) -  used to define DOM elements. 
- [JavaScript](https://www.javascript.com/)  -  used to help handle challenge member entry.
- [Django](https://www.djangoproject.com/) - Python Framework
- [Markdown](https://www.markdownguide.org/) Documentation within the readme was generated using markdown

## Fonts
 - [Montserrat](https://fonts.google.com/?query=montserrat)
 - [Helvtica](https://fonts.google.com/?query=helvetica)

## Tools
 - [Adobe XD](https://www.adobe.com/ie/products/xd.html)
 - [VS Code](https://code.visualstudio.com/)

## APIs
 - [Mailchimp Marekting API](https://mailchimp.com/developer/marketing/api/)
 - [Twillo Sendgrid](https://www.twilio.com/sendgrid/email-api)
 - [Stripe](https://stripe.com/)

## Testing

### Penetration Testing
Basic penetration testing was done to ensure that unauthenticated users can't access authenticated content and that permissionless users can't edit role based permission functions.

#### Testing Authenticated Routes
    1. Without logging in attempt to access the url "/dashboard"
    2. Using Postman try to send a POST request to the endpoint "/checkin/"
    
#### Result
User is redirected to the login page with the dashboard url set as the value of the "next" paramater in the current url - ***passed*** \
A response telling the user they are unauthenticated is returned - ***passed*** \

### Validation Testing

- [CSS Validator](https://jigsaw.w3.org/css-validator/) 
- [HTML Validator](https://validator.w3.org/) Note, because Alpine JS manipulate html element by placing aditional attributes on them such as "x-data" or ":class", there are returned as errors by the validator.
- [PEP8 Validator](https://www.pythonchecker.com/)

### Cross Browser and Cross Device Testing

| TOOL / Device                 | BROWSER     | OS         | SCREEN WIDTH  |
|-------------------------------|-------------|------------|---------------|
| real phone: iPhone 6          | chrome      | iOs        | XS 360 x 640  |
| dev tools emulator: iPhone5s  | chrome      | iOs        | XS 320 x 568  |
| dev tools emulator: pixel 2   | chrome      | android    | SM 411 x 731  |
| dev tools emulator: iPhone 8  | chrome      | iOs        | SM 411 x 731  |
| dev tools emulator: iPad      | chrome      | iOs        | MD 768 x 1024 |
| dev tools emulator: Surface   | chrome      | android    | MD 540 x 720  |
| dev tools emulator: iPad Pro  | chrome      | iOs        | LG 1024 x 1366|
| real computer: mac book pro   | safari      | Catalina   | XL 1400 x 766 |
| real computer: mac book pro   | chrome      | Catalina   | XL 1400 x 766 |

### Automated Testing
Due to the fact that there are only two data models and a relatively simple frontend, I did not find situations where automated testing such as integration testing was neccessary as the the app is generally not complex enough to have majorly conflicitng elements or many change breaking features.

### Manual Testing
Much of the app has been tested manually as follows:

#### 1. Newsletter form:
    1. Go to the Index page
    2. Try to submit the empty form and verify that an error message about the required fields appears
    3. Try to submit the form with an invalid email address and verify that a relevant error message appears
    4. Try to submit the form with all inputs valid and verify that a success message appears.
    5. Try to sign up as an already subscbribed user.

##### Results
* Index Page loads - ***passed***
* Form return visual feedback for required fields - ***passed***
* Form requests email address with '@' symbol be entered - ***passed***
* Form returns success message - ***passed***
* Form returns message stating that user is already subscribed - ***passed***

#### 2. Contact form:
    1. Go to the Index page.
    2. Try to submit the empty form and verify that an error message about the required fields appears.
    3. Try to submit the form with an invalid email address and verify that a relevant error message appears.
    4. Try to submit the form with all inputs valid and verify that a success message appears.

##### Results
* Index Page loads - ***passed***
* Form return visual feedback for required fields - ***passed***
* Form requests email address with '@' symbol be entered - ***passed***
* Form returns success message - ***passed***

#### 3. Registration Page:
    1. Go to the Registration page.
    2. Try to submit the empty form and verify that an error message about the required fields appears.
    3. Try to submit the form with an invalid email address and verify that a relevant error message appears.
    4. Try to submit form with mismatched passwords and verify mismatched password message.
    5. Try to submit the form with all inputs valid and verify that a success message appears.

##### Results
* Registration Page loads - ***passed***
* Form return visual feedback for required fields - ***passed***
* Form requests email address with '@' symbol be entered - ***passed***
* Form returns message that passowords do not match - ***passed***
* From returns success message and logs user in - ***passed***

#### 4. Login Page:
    1. Go to the Login page.
    2. Try to submit the empty form and verify that an error message about the required fields appears.
    4. Try to submit form with invalid credentials and verify error shows.
    5. Try to submit the form with all inputs valid and verify that a success message appears.

##### Results
* Login Page loads - ***passed***
* Form return visual feedback for required fields - ***passed***
* Message is displayed that credentials are invalid - ***passed***
* Form returns success message - ***passed***

#### 5. Dashboard Page:
    1. Go to Dashboard.
    2. Try to submit the empty form and verify that an error message about the required fields appears.
    3. Try to Edit a post and verify you are directed to the edit page with the correct post.
    4. Try to Delete a post.

##### Results
* Dashboard Page loads - ***passed***
* Form return visual feedback for required fields - ***passed***
* Button brings you to the edit page with the post content prefilled in the form - ***passed***
* Form returns success message that post was deleted - ***passed***

#### 6. Check In Functionality:
    1. Go to the Dashboard page.
    2. Try to checkin without an active membership.
    3. Try to checkin with an active membership.
    4. Try to cancel booking

##### Results
* Dashbuard Loads - ***passed***
* A message flashed saying a user needs an active membership to check in - ***passed***
* User is checked in and a message appears - ***passed***
* User is brought to confimration page and can cancel booking - ***passed***


#### 8. Logout Functionality:
    1. Click logout button.
  
##### Results
* User is redirected to index page and is logged out - ***passed***

#### 9. Conditional Rendering:
    1. As an unauthenitaced user check that navbar only displays Log In Button.
    2. As an authenitaced user check that navbar  displays Dashboard and Log Out Button.
 
##### Results
* Log In Button appears in navbar but not Dashboard or Log Out Buttons - ***passed***
* Dashboard and Log Out Buttons appears in navbar but not Log In Button - ***passed***

### Defect Tracking

### Defects of Note
The absolute position of the form on index, login and register can overlap the div below if the screen height is very small or push by other browser elements on mobile.

## Deployment

### Deploy Locally

To deploy locally:

1. In the terminal run the command
``` 
git clone https://github.com/slammer1870/execbjj-django.git 
```
2. In the root directory create your virtual environment and run
```
pip install -r requirements.txt
```
3. Create a .env file with the environemnt variables:\
> |        Variable       	|   Setting  	|
>|:---------------------:	|:----------:	|
>| DATABASE_URL                | YOUR_KEY   	|
>| SECRET_KEY        	    | YOUR_KEY   	|
>| MAILCHIMP_API_KEY        | YOUR_KEY    	|
>| MAILCHIMP_SERVER 	    | YOUR_KEY  	|
>| MAILCHIMP_LIST_ID        | 5000       	|
>| SECRET_KEY            	| YOUR_KEY  	|
>| SENDGRID_API_KEY    	    | YOUR_KEY  	|
>| STRIPE_API_KEY    	    | YOUR_KEY  	|
>| STRIPE_WEBHOOK_SECRET    	    | YOUR_KEY  	|
>| DEFAULT_FROM_EMAIL    	    | YOUR_KEY  	|

```
7. Run
```
READ_DOT_ENV_FILE=True python manage.py runserver
```

### Deploy To Heroku
To deploy to Heroku:

1. In the terminal run the command
``` 
git clone https://github.com/slammer1870/studious-lamp.git 
```
2. Login to Heroku and set up a new app
3. Under the Settings tab, click Reveal Config Vars
4. Set the config variables to be:
> |        Variable       	|   Setting  	|
>|:---------------------:	|:----------:	|
>| DATABASE_URL                | YOUR_KEY   	|
>| SECRET_KEY        	    | YOUR_KEY   	|
>| MAILCHIMP_API_KEY        | YOUR_KEY    	|
>| MAILCHIMP_SERVER 	    | YOUR_KEY  	|
>| MAILCHIMP_LIST_ID        | 5000       	|
>| SECRET_KEY            	| YOUR_KEY  	|
>| SENDGRID_API_KEY    	    | YOUR_KEY  	|
>| STRIPE_API_KEY    	    | YOUR_KEY  	|
>| STRIPE_WEBHOOK_SECRET    	    | YOUR_KEY  	|
>| DEFAULT_FROM_EMAIL    	    | YOUR_KEY  	|
5. Log in to Heroku, you can do this by running
```
heroku login
```
6. Clone the heroku repository
```
heroku git:clone -a 'your_app_name'
```
7. Add your files, commit and push to Heorku main:
```bash
$ git add .
$ git commit -am "initial heroku commit" 
$ git push heroku main
```

## Credits
The footer component, map and timetable was bootstrapped from [tailblocks.cc](https://tailblocks.cc/)

### Content
All of the copy on the website is written by me

### Media
Some of the photos are owned by [MaggieLeft](https://maggieleft.com/) the rest of the content is owned by ExecBJJ Ltd.

### Acknowledgments
I'd like to thank my mentor Malia for helping me!
