# trec-dd-jig

##### This is the readme file of  the user simulator (jig) package for the TREC 2016 Dynamic Domain (DD) Track.
##### The package is for research use only.

##### For technical questions, please send your request to google group https://groups.google.com/forum/#!forum/trec-dd

**************************************************************************

### What's inside the package:

* the jig (jig/jig.py)
* task measure scripts
* sample run files

**************************************************************************

### Requirements

#### 1. System requirements
- Works under Mac OS, Windows, and Linux.
- Python environment. (Works the best under Python 2.7)


#### 2. Download the TREC DD Topics:

- Topics (with ground truth) must be the one downloaded from NIST. (http://trec.nist.gov/act_part/tracks16.html)


### Install the Jig

#### 1. Download the jig package:

  ``` shell
    > git clone https://github.com/trec-dd/trec-dd-jig
  ```

#### 2. Quick install Python packages needed:

        > cd trec-dd-jig
        > sudo easy_install pip
        > sudo pip install -r requirements.txt


#### 3. Configuration and Setup
- Create your own directory to hold your trec-dd search system.
    ``` shell
        > mkdir your_dd_directory
    ```

- Put the jig package under your_dd_directory, that is,
  ``` shell
        > mv trec-dd-jig your_dd_directory/.
  ```

- Unzip and put the topics (with ground truth) file that you downloaded from NIST, under ~/your_dd_directory/trec-dd-jig/jig/topics/
  ``` shell
        > gunzip dd_topic_file.xml.gz
        > mv dd_topic_file.xml your_dd_directory/trec-dd-jig/topics/
  ```

- Setup database

  ``` shell
        > cd trec-dd-jig
        > sh jig/config.sh --topics topics/topic_file.xml
  ```
  This will set up a sqlite database at ./trec-dd-jig/jig/truth.db

 Congratulations for a successful installation!!

**************************************************************************
### Run the Jig
- Your systems should call python jig/jig.py to get feedback for each iteration of retrieval. The jig outputs a json dumped string. It provides feedback to your returned documents. Use the following command to call the Jig:

  ``` shell
    > python jig/jig.py -r runid -topic topic_id -docs docno1:rankingscore docno2:rankingscore docno3:rankingscore docno4:rankingscore docno5:rankingscore
  ```

    + where:

        - runid: An identifier used to declare the run
        - topic_id: the id of the topic you are working on
        - docno1, docno2 ...: the five document ids that your system returned. It needs to be the document ids in TREC DD datasets.
        - ranking score: the ranking score of the documents generated by your system

-  Suppose your run id is 'testrun'. Call the jig with the topic id, the run id, the ids of the 5 documents that your system retrieved together with their ranking scores:

    ``` shell
        > python jig/jig.py -runid testrun -topic DD16-1 -docs ebola-45b78e7ce50b94276a8d46cfe23e0abbcbed606a2841d1ac6e44e263eaf94a93:833.00 ebola-012d04f7dc6af9d1d712df833abc67cd1395c8fe53f3fcfa7082ac4e5614eac6:500.00 ebola-20d0e40dbc6f60c35f581f4025076a4400bd46fa01fa0bc8164de05b286e04f8:123.00 ebola-da1e8bbbb0c543df9be4d59b37558927ed5ee4238c861ce1205ed7b41140ad3a:34.00 ebola-9e501dddd03039fff5c2465896d39fd6913fd8476f23416373a88bc0f32e793c:5.00
    ```

- The jig will print the feedback on the screen. Each feedback is a json dumped string.

    ``` shell
    [
     {
         "topic_id": "DD15-1"
         "ranking_score": "833",
         "on_topic": "1",
         "doc_id": "1322120460-d6783cba6ad386f4444dcc2679637e0b",
         "subtopics": [
             {
                 "passage_text": "Federal judge Redden taking himself off the salmon case",
                 "rating": 3,
                 "subtopic_id": "DD15-1.1",
             },

             { ... }
         ],
     }
     { ... }
    ]

    ```
    + where:
        - docid: the id of a document
        - subtopic_id: the id of a relevant subtopic that the document covers
        - passage_text: the content of a relevant passage that the document covers
        - rating: the graded relevance judgments provided by NIST assessors. less than 2: marginally relevant, 2: relevant, 3: highly relevant, 4: key results. The relevance grades refer to the relevance level of the passage to a subtopic.
        - ranking score: the ranking score of a document provided by your system

- A run file will be automatically generated at the current directory with the runid as its name. This will be the run file that you submit to NIST later.

    ``` shell
        > cat ./testrun.txt

        > DD15-1 1322120460-d6783cba6ad386f4444dcc2679637e0b 833.00 1 DD15-1.1:3|DD15-1.4:2|DD15-1.4:2|DD15-1.4:2|DD15-1.4:2|DD15-1.4:2|DD15-1.2:2|DD15-1.2:2

        > DD15-1 1322509200-f67659162ce908cc510881a6b6eabc8b 500.00 1 DD15-1.1:3

        > DD15-1 1321860780-f9c69177db43b0f810ce03c822576c5c 123.00 1 DD15-1.1:3

        > DD15-1 1327908780-d9ad76f0947e2acd79cba3acd5f449f7 34.00 1 DD15-1.3:2|DD15-1.1:2

        > DD15-1 1321379940-4227a3d1f425b32f9f8595739ef2b8c3 5.00 0
    ``` 


    + where:
        - topic id: the id of the topic you are working on
        - docid: the id of a document
        - ranking score: the ranking score of a document provided by your system
        - on topic: 0 means the document is off topic, 1 means on topic
        - subtopic_id: the id of a relevant subtopic that your document covers
        - rating: the relevance grade provided by NIST assessors. -1/0/1: marginally relevant (Note that: ratings -1 or 0 or 1 all mean marginally relevant), 2: relevant, 3: highly relevant, 4: key results. The relevance grades refer to the relevance level of your document to the whole topic.

- Note that subtopic_ids are global ids, i.e., a certain topic might contain subtopic with id 12, 45, 101, 103...
- Everytime when you run 'jig/jig.py' for the same topic id, the run file will be automatically appended and the number of interaction iterations will increase by one. 


**************************************************************************


### Metrics
- We support a few metrics. The scripts for these metrics can be found at the ./scorer directory.
- You will need the actual qrels from NIST to evaluate your runs. Here we demonstrate how to use the scorers using a sample qrels file and a sample run file. Both files can be found at the ./sample/ directory.
    + qrels.txt: a sample qrels file
    + runfile: a sample run file
- How to run the scorers

    + Average Cube Test (ACT) and Cube Test (CT)

      ``` shell
        >$ perl cubeTest_dd.pl  ../sample_run/qrels.txt ../sample_run/runfile 50
      ```
        - where 50 is the default cutoff value of the number of iterations where you run cubetest over your results. You should try different cutoff values.

    + Alpha-nDCG per iteration and nERR-IA per iteration

      ``` shell
        >$ gcc -o ndeval ndeval_dd_all_iteration_detail.c -lm
        >$ ./ndeval  ../sample_run/qrels.txt ../sample_run/runfile
      ```

    + snDCG per iteration

      ``` shell
        >$ perl snDCG_per_iteration.pl  ../sample_run/qrels.txt ../sample_run/runfile 5
      ```

    + Precision (up to the current iteration)

      ``` shell
        >$ python precision.py -qrel ../sample_run/qrels.txt -run ../sample_run/runfile
      ```