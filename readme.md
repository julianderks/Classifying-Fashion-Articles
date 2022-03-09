# Python project that walks trough the full pipeline of a (simple) deep learning project

<center><img src="misc\MLOps_pipeline.png" width="800px" height="400px" /><center>

We will walk through all the steps of the machine learning pipeline and deploy a simple Convolutional Neural Network (CNN) that is able to classify fashion articles.

1. Collect image data of fashion articles from www.zalando.com with a webscraper
2. Preprocess and clean the data
3. Traing the CNN implemented with pytorch
4. Validate the CNN
5. Test the CNN
6. Deploy the CNN with Flask where an use can provide an image to
   be classified and where the results are stored in an SQL database
7. The collected data in the database can be used to improve the model
