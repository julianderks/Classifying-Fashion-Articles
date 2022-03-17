# Python project that walks trough the full pipeline of a (very simple) deep learning project

<center><img src="misc\MLOps_pipeline.png" width="500px" height="400px" /><center>

We will walk through all the steps of the machine learning pipeline and deploy a simple Convolutional Neural Network (CNN) that is able to classify fashion articles.

:heavy_check_mark: Collect image data of fashion articles from www.zalando.com with a webscraper :heavy_check_mark:
:heavy_check_mark: Preprocess and clean the data
:x: Traing the CNN implemented with pytorch
:x: Validate the CNN
:x: Test the CNN
:x: Deploy the CNN with Flask where an user can provide an image to
be classified and where the results are stored in an SQL database
:x: The collected data in the database can be used to improve the model
