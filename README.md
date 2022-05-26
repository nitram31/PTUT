# PTUT

## Tutored project
This pipeline is used to predict and annotate presequence-less transmembrane mitochondrial proteins, it produces a 31 column table that includes all the information used to predict the likelyhood of a protein being in a particular class.

### Table description
The first column is the name of the sequence, including its uniprot ID. 

The second and third are the TargetP prediction :'targetp_pred' ; OTHER, SP (Signal Peptide), MT (Mitochondrial Transfer = presequence) and its score, 'targetp_pred' between 0 and 1 that represents the score of the prediction.

The fourth, fifth an sixth column are the transmembrane segment prediction softwares :'tmhmm_tm_pred_', 'HMMTOP_tm_pred'(http://www.enzim.hu/hmmtop/html/submit.html) and 'DeltaG_tm_pred'(https://dgpred.cbr.su.se/index.php?p=fullscan) like the other two softwares it represents the predicted topology of the protein using a list of numbers and letters :

- Prediction of TM with tmhmm, HMMTOP, and DeltaG
* i: inside
* o: outside
* M: membrane

Exemple : TMHMM prediction for BCS1 ⇒ ['i', 1, 50, 'M', 51, 73, 'O', 74, 456]
* 1 to 50 : inside (on the matrix side)
* 51 to 73 : transmembrane domain
* 74 to 456 : outside (intermembrane)

The eigth column is the hydrophobicity score associated with a deltaG predicted TM segment, 'deltaG_pred_score' : it represents the corresponding apparent free energy difference and in general a positive score means a less stable TM segment.


There are 5 columns per TM segment predicting software associated with charge : two per side of the TM segment, we take the charge of the 5 and 10 amino acids located before and after the TM segment or each of the TM segment if we have more. The last column is the bias of charge between two sides of a TM segment : we look at the charge caculated above and we see if one side has a higher positive charge tha the other, leading to a bias that could lead to a protein being imported positive side first.

We included in a column a uniprot link.

Another column also includes the high confidence localization of the protein extracted from Morgenstern M, et al. (2017).

the column 'class' is the predicted class given by the pipeline based on the number of TM segment and the targetP prediction: class 1 is 1 TM segment without presequence, class 2 is 2 and without aswell and class 3 is 2 TM and above with a presequence.

Associated with the class is the column 'score' : if one protein is predicted as class 1 but hasn't any of the other characteristics it's score will be lower than a protein predicted with a charge bias


 







