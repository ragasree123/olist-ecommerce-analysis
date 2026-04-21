# Olist E-commerce Analysis Analysing 100,000+ real orders from Olist  Brazil's largest e-commerce marketplace (2016–2018). 
## Business Questions 
1. Which product categories have the worst delivery delays? 
2. Does late delivery cause 1-star reviews?
3. Which states and categories drive the most revenue?

## Key Findings — Week 1
- **bed_bath_table** leads in order volume (11,115 orders)
  but **computers_accessories** has nearly double the avg
  order value (R$158 vs R$83)
- **92.1% of orders arrive early** — Olist uses conservative
  delivery estimates (mean = 12 days early)
- Only **6.6% of orders are late** — but the worst case
  was 189 days overdue
- **58,247 reviews** have no written comment — star rating
  is the only reliable satisfaction metric

## Tools Used
Python · pandas · matplotlib · SQL · Excel · Power Query

## Project Status
Week 1 complete — foundations, EDA, data cleaning done
Week 2 starting — delivery performance deep dive

## Dataset
[Brazilian E-Commerce Public Dataset — Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

## Screenshots
![Top 10 Categories](images/top10_categories.png)
![Delivery Delay Distribution](images/delivery_delay_dist.png)
