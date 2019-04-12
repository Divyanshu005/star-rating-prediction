# star-rating-prediction

This is the code for the paper titled 'Leveraging Aspect Phrase Embeddings for Cross-Domain Review Rating Prediction'.

## Introduction

Online review platforms are a popular way for users to post reviews by expressing their opinions towards a product or service, as well as they are valuable for other users and companies to find out the overall opinions of customers. These reviews tend to be accompanied by a rating, where the star rating has become the most common approach for users to give their feedback in a quantitative way, generally as a likert scale of 1-5 stars. In other social media platforms like Facebook or Twitter, an automated review rating prediction system can be useful to determine the rating that a user would have given to the product or service. Existing work on review rating prediction focuses on specific domains, such as restaurants or hotels. This, however, ignores the fact that some review domains which are less frequently rated, such as dentists, lack sufficient data to build a reliable prediction model. In this paper, we experiment on 12 datasets pertaining to 12 different review domains of varying level of popularity to assess the performance of predictions across different domains. We introduce a model that leverages aspect phrase embeddings extracted from the reviews, which enables the development of both in-domain and cross-domain review rating prediction systems. Our experiments show that both of our review rating prediction systems outperform all other baselines. The cross-domain review rating prediction system is particularly significant for the least popular review domains, where leveraging training data from other domains leads to remarkable improvements in performance. The in-domain review rating prediction system is instead more suitable for popular review domains, provided that a model built from training data pertaining to the target domain is more suitable when this data is abundant.

## Data declaration

We are not allowed to redistribute the data, but the original sources of the datasets are cited in the paper. Datasets can be directly found from [Yelp](https://www.yelp.com/dataset/challenge), [Amazon](https://registry.opendata.aws/) and [TripAdvisor](https://www.tripadvisor.com/ShowTopic-g1-i12105-k10292711-Datasets_from_tripadvisor-TripAdvisor_Support.html).

## File description

* 01.get.pos.py/02.get.phrases.py/03.get.posneg.phrases.py: extract review texts to generate the sentiment phrases as the first step.

* classification.py/cross.classification.py: classification.py is for in-domain and cross.classification.py is for cross-domain experiment.
* 'python print.results.py maxent' for printing the results.
* get.top.posneg.py

## Running
To run the classifier:

python all.nonstruct.classification.py [features] [time] [window] [months]

where: [features] is the feature set, e.g. multiw2v [time] is the time in seconds used for the classification, i.e. the earliness of predictions [window] is the percentage of the data used as the sliding window, ranging from 0 to 1 [months] is the number of months used for training, from 1 to 24

## License
[MIT](https://opensource.org/licenses/MIT)
