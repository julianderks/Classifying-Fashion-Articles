<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/julianderks/Classifying-Fashion-Articles">
    <img src="misc/images/logo.png" alt="Logo" width="240" height="240">
  </a>

  <h3 align="center">Fashion Article Classifier</h3>

  <p align="center">
    We will walk through all the steps of the machine learning pipeline and deploy a simple Convolutional Neural Network (CNN) that is able to classify fashion articles.
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

**Note: The is a project under construction, many components will not work yet.**

A self-study project with the aim to implement every step of an ML project (i.e. from data collection to production) and to get more familiar with best practices around git repositories (like having a proper readme.md :partying_face:). Specifically, a webscraper is build to extract packshots of fashion articles from [Zalando](https://www.zalando.nl/kleding/). The extacted data is preprocessed on which a (very simple) pytorch based CNN is trained. The pytorch code will contain alot of boiler plate code such that it can be used in future pytorch projects. The trained model will eventually be deployed on an web application using Flask, users will be able to interact with it and data is stored to a database.

<p align="right">(<a href="#top">back to top</a>)</p>

## Installation

1. Clone the repo

   ```sh
   git clone https://github.com/julianderks/Classifying-Fashion-Articles.git
   ```

2. Go to project directory

   ```sh
   cd Classifying-Fashion-Articles
   ```

3. Create and activate new vertual environment (recommended)

   ```sh
   virtualenv venv
   ```

   ```sh
   source venv/bin/activate
   ```

4. Install all dependencies

   ```sh
   pip install -r requirements.txt
   ```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

TO DO

Additional screenshots, code examples and demo of scraping / training / using the webapp.

### Webscraper

Go to the [webscraper readme](https://github.com/julianderks/Classifying-Fashion-Articles/tree/main/code/webscraper)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

- Collect image data of fashion articles from [Zalando](https://www.zalando.nl/kleding/) with a webscraper :heavy_check_mark:
- Traing/Validating/Testing the CNN implemented with pytorch :x:
  - Not finished
- Deploy the CNN with Flask where an user can provide an image to be classified and where the results are stored in a database :x:
  - Made a tiny start, currently investing time in learning more about HTML/CSS and FLASK

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

Linkedin - [Julian Derks](https://www.linkedin.com/in/julianderks/)

Project Link: [https://github.com/julianderks/Classifying-Fashion-Articles](https://github.com/julianderks/Classifying-Fashion-Articles)

<p align="right">(<a href="#top">back to top</a>)</p>
