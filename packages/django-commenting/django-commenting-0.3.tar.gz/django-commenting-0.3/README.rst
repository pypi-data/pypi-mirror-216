=================================
A Django Nested Commenting App
=================================

Commenting is a Django app to add nested comment functionality to you django web application.

Detailed documentation is in the "docs" directory.

Quick start
===========

1. Add "commenting" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        'commenting',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('commenting/', include(('commenting.urls', 'commenting'), namespace='commenting')),

3. Run ``python manage.py migrate`` to create the polls models.

4. Start the development server ``python manage.py runserver`` and 
    visit ' http://127.0.0.1:8000/admin/ 'to see whether comment model has been added successfully or not.

5. In your object(say Post) detail page add 
    ' {% load comment_form_tag %} ' below {% extend %} if there is.

6. Now load the comment application in the template using 
    ' {% render_comment_form post %} ''