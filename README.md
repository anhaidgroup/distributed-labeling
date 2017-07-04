# distributed-labeling
# Introduction
This document briefly describes the web-based labeling process to map drug pairs between Free Pharma and SHP data sets.

# Navigating to Labeling Page
The web-page to label drug pairs can be reached at [pradap-www.cs.wisc.edu/mfc_web](pradap-www.cs.wisc.edu/mfc_web).

# Page Contents
Once the user goes to the labeling page URL from the web browser, he/she will displayed a page like this

![Page Contents](https://github.com/slamphear/distributed-labeling/raw/master/images/page_contents.png)

The page contains three panels:
* Main label panel
* Summary label panel
* Filter label panel

## Main Label Panel
This panel serves two main purposes:

Aid the user in labeling the drug pair
Save the labels

A blown up main label panel is shown below

![Main Label Panel](https://github.com/slamphear/distributed-labeling/raw/master/images/main_label_panel.png)

The panel primarily contains a table with drug pair information, labeling options and option to save.

Each drug pair is displayed as two rows one below the other. This is followed by a bunch of labels that the user can select. For conciseness, only a subset of columns are displayed in the table. If the user wants to look at all the columns, he/she can click on 'View Tuple Pairs' button. This will open a new tab with detailed information of tuple pairs.

The user can periodically save the labels by clicking on ‘Save and Continue’ button at the top right side of the panel.

Note: Each page displays only a maximum of 20 rows. The user can move to subsequent pages by scrolling down the page and clicking on the next button as shown below

![Previous and Next Buttons](https://github.com/slamphear/distributed-labeling/raw/master/images/previous_and_next_buttons.png)

Further, the displayed table is both horizontally and vertically scrollable. The horizontal scroll bar is at the bottom of the page
 
## Summary Label Panel
This panel shows a summary counts of different label types saved. Note that, this panel gets updated only when the user saves the labels by clicking on ‘Save and Continue’ button.
An example screenshot is shown below:

![Summary Label Panel](https://github.com/slamphear/distributed-labeling/raw/master/images/summary_label_panel.png)

## Filter Label Panel
The panels helps the user to select a subset of label types and view or re-label them in the main panel. The user can select multiple label types. 
An example of selection and resulting main panel will look like this

# Labeling Process
In the main panel, the user can view the drug pair and select the appropriate label type. The user is displayed with 7 label types:
1. Unlabeled
2. User-Yes
3. User-No
4. User-Unsure
5. Expert-Yes
6. Expert-No
7. Expert-Unsure

The Non-expert user is typically a non-technical user but has some knowledge about drugs. Such users are expected to typically choose among User-Yes, User-No, User-Unsure.They would typically label ‘Unlabeled’ label types.  If they definitely know that the drug pair is a match then they will choose User-Yes. If they definitely know that the drug pair is a non-match then they will choose User-No. If they are unsure they will choose User-Unsure.

The expert-users, as the name suggests are experts with significant knowledge about drugs. Such users are expected to choose among Expert-Yes, Expert-No, Expert-Unsure. They would typically verify non-expert user labels and re-label ‘User-Unsure’ or 'Unlabeled' label types.If they definitely know that the drug pair is a match then they will choose Expert-Yes. If they definitely know that the drug pair is a non-match then they will choose Expert-No. If they are unsure they will choose Expert-Unsure (say for instance there were lots of missing values for that drug pair).

During the labeling process it is highly recommended  to save the table frequently and continue with labeling. The data gets saved in the database, hence the labeling process can be resumed later as per user’s convenience.

*Note: Currently, the web page does not provide different access to non-expert or expert users. It is expected that the non-expert users and expert users share the same url.  It is also expected that the non-expert users do not re-label expert user labels.*
