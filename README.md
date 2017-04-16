# What Is My Fish?
For decades, our Lake Erie’s ecosystems have been thrown out of balance as invasive fish outcompete native fish for food, eat native fish eggs, and uproot plants utilized by other animals for food or shelter.  Despite the Department of Natural Resources’ (DNR) efforts, lakes threaten to be overfished by those oblivious or non-compliant with size and count limits.  

Our great lakes- a vital component of our communities’ long term economic survival- are threatened.

Fish.io.ai has set out to solve these problems through WhatIsMyFish.net, a free to use mobile web application that empowers users to save our lake.  With the click of a mobile camera and the power of deep learning, users are told what fish they caught, whether it is invasive or not, and are presented the fishing regulations for the area they are fishing.

Every photo educates fishermen on whether a specific fish should be returned to the lake and the DNR fishing rules for specific species.  Invasive species will be identified and removed.  Further, young fish not ready for harvest will be returned to the water and given the opportunity to reproduce, ensuring the long-term sustainability of the species.  

Experts can contribute to the accuracy of the deep learning model by viewing uploaded images and either confirming or making corrections to species predictions using our user interface. If a new species is caught, our app will quickly alert the DNR.  

When individuals utilize the application, what fish was caught, where it was caught, and when it was caught is stored to curate a dataset like none other.  This new data will empower researchers to ask and answer questions pertaining to fish species populations and activity based on location, weather conditions, time of day/year, and other questions beyond our imaginations.  The application will provide meaningful contributions to short and long term research endeavors for generations.

*Fish.io.ai is comprised of 4 Data Scientists/IT professionals passionate about data, machine learning, and achieving large scale societal impact.  We are enthusiastic about bringing deep learning to the great outdoors to solve our community's greatest problems. Will you join us?*


# fish.io.ai
Krillin' it since 2017

To launch app make sure to have a conda env called "fishr" with the necessary dependencies.

```bash
# in dev
./fishr-cli.sh --dev --start
# in prod
./fishr-cli.sh --prod --start
```

To kill app:

```bash
# in dev
./fishr-cli.sh --dev --kill
# in prod
./fishr-cli.sh --prod --kill
```
