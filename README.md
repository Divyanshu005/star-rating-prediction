# star-rating-prediction

This is the code for the paper titled 'Leveraging Aspect Phrase Embeddings for Cross-Domain Review Rating Prediction'.

## Introduction

Online review platforms are a popular way for users to post reviews by expressing their opinions towards a product or service, as well as they are valuable for other users and companies to find out the overall opinions of customers. These reviews tend to be accompanied by a rating, where the star rating has become the most common approach for users to give their feedback in a quantitative way, generally as a likert scale of 1-5 stars. In other social media platforms like Facebook or Twitter, an automated review rating prediction system can be useful to determine the rating that a user would have given to the product or service. Existing work on review rating prediction focuses on specific domains, such as restaurants or hotels. This, however, ignores the fact that some review domains which are less frequently rated, such as dentists, lack sufficient data to build a reliable prediction model. In this paper, we experiment on 12 datasets pertaining to 12 different review domains of varying level of popularity to assess the performance of predictions across different domains. We introduce a model that leverages aspect phrase embeddings extracted from the reviews, which enables the development of both in-domain and cross-domain review rating prediction systems. Our experiments show that both of our review rating prediction systems outperform all other baselines. The cross-domain review rating prediction system is particularly significant for the least popular review domains, where leveraging training data from other domains leads to remarkable improvements in performance. The in-domain review rating prediction system is instead more suitable for popular review domains, provided that a model built from training data pertaining to the target domain is more suitable when this data is abundant.

## Data declaration

We are not allowed to redistribute the data, but the original sources of the datasets are cited in the paper. Datasets can be directly found from [Yelp](https://www.yelp.com/dataset/challenge), [Amazon](https://registry.opendata.aws/) and [TripAdvisor](https://www.tripadvisor.com/ShowTopic-g1-i12105-k10292711-Datasets_from_tripadvisor-TripAdvisor_Support.html).

## File description

* 01.get.pos.py/02.get.phrases.py/03.get.posneg.phrases.py: To extract review texts to generate the sentiment phrases as the first step.
* get.top.posneg.py: To get some top phrases in different domains.
* classification.py/cross.classification.py: classification.py is the classifier for in-domain and cross.classification.py is the one for cross-domain experiment.
* print.cross.results.py/print.results.py: To print the results. It could be run like 'python print.results.py maxent'


## License
[MIT](https://opensource.org/licenses/MIT)
