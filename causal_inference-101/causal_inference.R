###set up ##
setwd('/Users/snelson/projects/causal_inference')
install.packages("vars")
install.packages("arm")
install.packages("ggplot2")
library(vars)
library(arm)
library(ggplot2)

## correlated time series ##
corr_data<-read.table('beer_pizza.csv', sep=",", header=TRUE, stringsAsFactors=FALSE)
corr_data$dt<-as.POSIXct(strptime(corr_data$dt, format='%Y-%m-%d %H:%M:%S'))

#plot the TS
par(mfrow=c(2,1))
plot.ts(corr_data$beer)
plot.ts(corr_data$pizza)

#plot correlations
plot(corr_data$beer, corr_data$pizza)

#calc correlations
cor(corr_data$beer, corr_data$pizza, method="pearson")
cor(corr_data$beer, corr_data$pizza, method="spearman")
cor(corr_data$beer, corr_data$pizza, method="kendall")


######### granger causality #########
## time series overview here: http://cran.r-project.org/web/views/TimeSeries.html ##

x<-as.matrix(corr_data[,c("beer", "pizza")])
var.2c <- VAR(x, p = 2, type = "const")
summary(var.2c)
causality(var.2c, cause = "beer")
causality(var.2c, cause = "pizza")


######## sample size #####
### sample size calcs for proportion
n<-seq(1000, 10000, 1000)

power_calc_prop<-function(x){
  res<-power.prop.test(n = x, p1 = 0.503, power=0.8)
  return (res$p2)
}

plot_data<-as.data.frame(cbind(n, sapply(n, power_calc_prop)-0.503))
names(plot_data)<-c("n","Change in Positive Body Image Proportion")

plot(x=plot_data[,1], y=plot_data[,2], type="b", xlab="# of Responses", 
     ylab="Required Change for Stat. Sig.")

prop.test(x=c(2506, 202783), n=c(5527, 403133))
res<-prop.test(x=c(2506, 202783), n=c(5527, 403133))
0.5030176+res$conf.int[2]
0.5030176+res$conf.int[1]


### propensity score matching ###
data(lalonde)
help(lalonde)
lalonde$re74<-log(lalonde$re74+.01)
lalonde$re75<-log(lalonde$re75+.01)
lalonde$re78<-log(lalonde$re78+.01)
fit<-glm(treat~age + as.factor(educ) + black + hisp + married +  re74  + re75+
             u74 + u75, data=lalonde, family=binomial(link="logit"))
pscores<-predict(fit, type="link")
matches<-matching(z=lalonde$treat, score=pscores)
matched<-lalonde[matches$matched,]

# balance check!
b.stats <- balance(lalonde, matched, fit)
print(b.stats)
plot(b.stats)

#propensity score to assess coverage
data=cbind(as.data.frame(pscores), as.factor(lalonde$treat))
names(data)<-c("pscores", "treat")
qplot(pscores, data=data, geom="density", fill=treat, alpha=I(0.2), 
      main="Distribution of Propensity Scores", xlab="Propensity Score", 
      ylab="Density", xlim=c(-3,3))

matched_data<-cbind(as.data.frame(pscores[row.names(matched)]), 
                    as.data.frame(as.factor(matched$treat)))
names(matched_data)<-c("pscores", "treat")
qplot(pscores, data=matched_data, geom="density", fill=treat, alpha=I(0.2), 
      main="Distribution of Propensity Scores", xlab="Propensity Score", 
      ylab="Density", xlim=c(-3,3))

## compare original and adjusted regressions
reg.orig<-lm(re78~treat + age + as.factor(educ) + black + hisp + married + re74 + re75 + 
                     u74 + u75, data=lalonde)
reg.adj<-lm(re78~treat + age + as.factor(educ) + black + hisp + married  + re74 + re75 + 
               u74 + u75, data=matched)
summary(reg.orig)
summary(reg.adj)