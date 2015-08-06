---
title: "ab_testing"
author: "snelson"
date: "August 6, 2015"
output: html_document
---

# A/B Testing

This RST will attempt to cover a lot of ground in a short amount of time.  Here are the topics:

* A/B testing (design of experiments)
* Multiple hypothesis testing (controlling for data-snooping bias)
* Multi-armed bandits (adaptive testing)

## 1) AB Testing

###Problem
- We have formed a hypothesis and we want to test whether it's true using a controlled experiment

###Solution strategy
- We run a randomized controlled experiment, which consists of applying a control to the control group, and a treatment to the treatment group, where subjects are randomly assigned to either the treatment or control group, and the group sizes are large enough to ensure statistical significance. We compare the outcomes from both groups to evaluate the impact (lift) of the treatment.

###Method
1. Design experiment:
  - Identify factors and levels for the treatment
  - Sample size calculations
2. Randomize assignment of patients
3. Run experiment
4. Evaluate results

###Example: Ads

Curate an audience by retrieving a list of Twitter user_ids:
```
#bash code to retrieve follower_ids and concatenate into a list
#twurl /1.1/followers/ids.json?screen_name=s1nelson > s1nelson_followers.txt
#twurl /1.1/followers/ids.json?screen_name=jrmontag > jrmontag_followers.txt
#twurl /1.1/followers/ids.json?screen_name=kolb > kolb_followers.txt
#twurl /1.1/followers/ids.json?screen_name=drkippy > drskippy_followers.txt
#twurl /1.1/followers/ids.json?screen_name=notFromShrek > fiona_followers.txt
#find . -name "*followers*" | xargs -I {} cat {} | jq .ids[] | sort | uniq > ta.txt
#wc -l ta.txt
```

Sample size calculations:
```{r}
#sample size calc
#power.prop.test
#https://stat.ethz.ch/R-manual/R-devel/library/stats/html/power.prop.test.html
# need a baseline estimate. e.g. p=0.03

#test of equal proportions
#prop.test 
#https://stat.ethz.ch/R-manual/R-devel/library/stats/html/prop.test.html


#with a baseline rate of 0.03 and we want to detect a improvement of 0.02 --> ## #need 1186*2 => sample size 2372
power.prop.test(p1=0.03, p2=0.05, power = .80, sig.level=.05, alternative="one.sided")

#with a baseline rate of 0.03 and we want to detect a improvement of 0.01 
#need 4175*2 => sample size 8350
power.prop.test(p1=0.03, p2=0.04, power = .80, sig.level=.05, alternative="one.sided")

#sensitivity of required sample size to p2, assuming baseline of 0.03
power_calc<-function(p2){
  a<-power.prop.test(p1=0.03, p2=p2, power = .80, sig.level=.05, alternative="one.sided")
  return(a$n*2)
}
c<-seq(0.04, 0.10, 0.01)
res<-sapply(c, power_calc)
plot(x=c, y=res, type="l", xlab="p2", ylab="sample size", main="sample size w/ baseline of 0.03")
```


## Design of Experiments
[Ad 1](https://twitter.com/s1nelson/status/623875993371971584)
[Ad 2](https://twitter.com/s1nelson/status/623877238816047105)

- Factors + Levels

![alt text](/Users/snelson/projects/ab_testing/1-IMG_4228.JPG)

- Design:
    - Varying 1 factor at a time: requires 16 runs
    
![alt text](/Users/snelson/projects/ab_testing/FullSizeRender.JPG)

    - Factorial Design: requires only 8 runs
    
![alt text](/Users/snelson/projects/ab_testing/2-IMG_4231.JPG)

    - Interactions
  
## Analysis
```{r}
# analyze results
# load data from sample Twitter Ads campaign
t<-seq(1,15)
imp_img<-c(89,92,57,49,44,152,11,0,0,0,0,0,0,0,0)
eng_img<-c(10,8,0,0,2,5,1,0,0,0,0,0,0,0,0)
imp_no_img<-c(58,217,0,0,0,0,0,0,0,0,0,0,0,0,0)
eng_no_img<-c(2,16,0,0,0,0,0,0,0,0,0, 0,0,0,0)
data<-data.frame(t, imp_img, eng_img, imp_no_img, eng_no_img)

# t-test assumes completely randomized design
prop.test( c(sum(data$eng_img), sum(data$eng_no_img)), 
           c(sum(data$imp_img), sum(data$imp_no_img)))

#adjusting for the impression bias 
#phats
overall_eng_rate_img<-sum(data$eng_img)/sum(data$imp_img)
overall_eng_rate_no_img<-sum(data$eng_no_img)/sum(data$imp_no_img)
#se_phats
se_phat_img<-((overall_eng_rate_img*(1-overall_eng_rate_img))/sum(data$imp_img))^0.5
se_phat_no_img<-((overall_eng_rate_no_img*(1-overall_eng_rate_no_img))/sum(data$imp_no_img))^0.5
#adj phats
adj_phat_img<-overall_eng_rate_img/se_phat_img
adj_phat_no_img<-overall_eng_rate_no_img/se_phat_no_img
```

Risk adjusted p_hat_img: `r adj_phat_img` 
Risk adjusted p_hat_img: `r adj_phat_no_img` 

Ratio of performance metrics. Image improves baseline by 20%:
Ratio: `r adj_phat_img/adj_phat_no_img`

### Analysis of Variance
- What if there is variation in the day-of-week?
- This implies a need for [blocking](https://en.wikipedia.org/wiki/Randomized_block_design)
- Not sure what the "correct" strategy is (since we have impressions which depends on ad quality), but one possibility is to calculate per-day adjusted phats and run  ANOVA on this variable, with blocking factor=time period, and treatment=ad:

```{r}
##anova analysis
a<-data[,(1:3)]
a$img<-1
names(a)<-c("t", "imp", "eng", "img")
b<-data[,c(1,4,5)]
b$img<-0
names(b)<-c("t", "imp", "eng", "img")
data2<-rbind(a,b )
data2$img<-as.factor(data2$img)
data2$t<-as.factor(data2$t)
data2$phat<-data2$eng/data2$imp
data2$adj_phat<-data2$phat / (( data2$phat* (1-data2$phat) /data2$imp )**0.5)
data2
fit<-aov(adj_phat~t+img, data=data2)
summary(fit)
```

###Diff-in-Diff
* If we can take the pre-campaign levels of engagement for each group, we can calculate engagement uplift from each ad, relative to the pre-test levels for each group
* This controls for any systematic bias in the responses of each group

***********

## 2) Multiple Hypothesis Testing

###Problem
- if we run many tests, some will pass by chance alone
- hypothesis testing and p-values are designed for a single test

P(at least 1 significant result)=1-P(no sig results)
=1-(1-.05)**20
~=0.64

###Methods
- *Bonferroni correction* (statistics):  Penalize the p-value required for a result to be deemed signficiant
- *False discovery rate* (statistics): control the expected proportion of rejected null hypotheses that were incorrect rejections
- *Optimal discovery procedure* (genetics): maximizes the number of expected true positives for each fixed number of expected false positives
- *Reality Check / Superior Predictive Ability* (econometrics): correct for data-snooping bias -- does a given strategy really outperform the benchmark?
  
###Example
See this [set of lecture notes]: (http://www.stat.berkeley.edu/~mgoldman/Section0402.pdf):




```{r}
#simulate first 900 w/ standard normal, last 100 w/ mean 3
x <- c(rnorm(900), rnorm(100, mean = 3))
#calc p-values
p <- pnorm(x, lower.tail = F)
```

**No corrections**:
```{r}
test <- p > 0.05
summary(test[1:900])
summary(test[901:1000])
```

False positive rate: `r as.numeric(summary(test[1:900])[2])/900`

False negative rate: `r as.numeric(summary(test[901:1000])[3])/100`

**Bonferroni correction**:
```{r}
bonftest <- p > 0.00005
summary(bonftest[1:900])
summary(bonftest[901:1000])
```

False positive rate: `r as.numeric(summary(bonftest[1:900])[2])/900`

False negative rate: `r as.numeric(summary(bonftest[901:1000])[3])/100`

We've reduced false positives but increased our false negatives

**False Discovery Rate**:
Sort the pvalues; See if the k-th p-value is greater than k*.05 / 1000:
```{r}
psort <- sort(p)
fdrtest <- NULL
for (i in 1:1000)
fdrtest <- c(fdrtest, p[i] > match(p[i],psort) * .05/1000)
summary(fdrtest[1:900])
summary(fdrtest[901:1000])
```

False positive rate: `r as.numeric(summary(fdrtest[1:900])[2])/900`

False negative rate: `r as.numeric(summary(fdrtest[901:1000])[3])/100`
  
***********

## 3) Multi-armed Bandit (Adaptive Testing)

###Problem
- Let's say we have a slot machine with 3 arms (A,B,C)
    - We choose A and it wins --> does that mean we should always choose A?
- Multi-armed bandit:
    - Sample strategies proportional to their posterior probability of being "the best"
    - Balances "learn vs earn" or "explore vs exploit" of the unknown payoff distribution of different strategies
- How is this different than a randomized controlled trial?
    - RCT attempts to create balance across the differnet treatments to accurately estimate the effects of each treatment
    - MAB doesn't waste budget on estimating effects of bad treatments; it allocated those resources to good strategies in an optimal way
    
###Solution Strategy
See [this paper](http://www.economics.uci.edu/~ivan/asmb.874.pdf)

###Example

```{r}
#install.packages("bandit")
library(bandit)
x=c(10,20,30,33)
n=c(100,102,120,130)

#naive p, normalized
x/n / sum(x/n)

#binomial bandit -- number of times this strategy is best
round(best_binomial_bandit(x,n), 3)

#binomial bandit by simulation
round(best_binomial_bandit_sim(x,n, ndraws=1000), 3)

#i found this counter-intuitive at first
# but now it makes sense. The small sample arm 
# still has a top of upside potential that it could be >>>.01
# the large sample arm we have a pretty high certainty ==.01
x=c(10,20, 30, 40)
n=c(100,200,300,400)
x/n / sum(x/n)
best_binomial_bandit(x,n)
best_binomial_bandit_sim(x, n)
best_binomial_bandit_sim(c(2,20),c(100,1000), alpha = 2, beta = 5)

#quick look at the various shapes of the beta distribution as we change the shape params:
AlphaBeta = cbind(alpha=c(0.5,5,1,2,2),beta=c(0.5,1,3,2,5))
M = nrow(AlphaBeta)
y= matrix(0,100,ncol=M)
x = seq(0,1,length=100)
for (i in 1:M) y[,i] = dbeta(x,AlphaBeta[i,1],AlphaBeta[i,2])
matplot(x,y,type="l", ylim = c(0,3.5), lty=1, lwd=2)
```
