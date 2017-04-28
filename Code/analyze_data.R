library(tidyverse)
library(stringr)

###### Data fang et al 2012 ###################

Data_fang <- read_csv("../Data/data_retractions.csv")

fab_str <- "(fabricated|fak[eing]+|fabricati[ong]+)"
fals_str <- "(falsifying|falsified|falsification|false|manipulated|manipulation|biasing|tamper[ing]?)"
data_str <- "(data|report[s]?|experiment[s]?|research|result[s]?)"
image_str <- "(figure[s]?|image[s]?)"
tags <- c(paste(c("(.*",fab_str,"[^\\.]*",data_str,".*|",data_str,"[^\\.]*",fab_str,".*)"), collapse=""),
          paste(c("(.*",fals_str,"[^\\.]*",data_str,".*|",data_str,"[^\\.]*",fals_str,".*)"), collapse=""),
          paste(c("(.*",fab_str,"[^\\.]*",image_str,".*|",image_str,"[^\\.]*",fab_str,".*)"), collapse=""),
          paste(c("(.*",fals_str,"[^\\.]*",image_str,".*|",image_str,"[^\\.]*",fals_str,".*)"), collapse=""))
                
tags_names <- c("fabricated_data", "falsified_data", "fabricated_image", "falsified_image")

Data_fang <- Data_fang %>% mutate(reason = map_chr(`Secondary Source`, function(a){
    str_trim(paste(ifelse(rowSums(!is.na(str_match(a, tags))) > 0 , tags_names, ""), collapse = " "), "both") })) %>% mutate(reason = factor(reason, labels = c("other","fabricated data", " fabricated and falsified data", " fabricated and falsified image", "falsified data", " falsified image")))

Data_fang <- Data_fang %>% mutate(Period = cut(`Year Published`, breaks = 4))
Data_fang %>% group_by(Period, reason) %>% summarise(n = n()) %>% mutate(freq = n / sum(n)) %>% ggplot(aes(x = reason, y = freq, fill = Period)) + geom_bar(stat = "identity", position = "dodge") + theme_bw() + theme(axis.text.x = element_text(angle = 45, hjust = 1))

ggsave("../figures/plot_fang_fraud.png")

## by journal
Data_fang %>% ggplot(aes(x = Journal))  +geom_bar(aes(fill = `Final Reason for Retraction`)) + coord_flip() + theme_bw()

########## data ORI ##########################################

Data_ori <- read_csv("../Data/data_ori.csv")
Data_ori <- Data_ori %>% mutate(Period = cut(year, breaks = 3), reason = factor(reason, labels = c("fabricated and falsified data", "fabricated and falsified data and image", "fabricated and falsified data and falsified image", "falsified data", "falsified data an fabricated image", "falsified data and fabricated and falsified image", "falsified data and image"))) 

Data_ori %>% group_by(Period, reason) %>% summarise(n = n()) %>% mutate(freq = n / sum(n)) %>% ggplot(aes(x = reason, y = freq, fill = Period)) + geom_bar(stat = "identity", position = "dodge") + theme_bw() + theme(axis.text.x = element_text(angle = 45, hjust = 1))

ggsave("../figures/reason_retractions_ori.pdf")
###### retraction watch #######

Data_rw <- read_csv("../Data/retraction_watch.csv")

Data_rw %>% ggplot(aes(x = field, y = n_retractions)) + geom_bar(stat = "identity") + theme_bw() + coord_flip() + ylab(label = "number of retractions")

ggsave("retractions_by_field.png")
