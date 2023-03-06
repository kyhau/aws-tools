# RDS CA-2019

References:
1. https://aws.amazon.com/blogs/aws/urgent-important-rotate-your-amazon-rds-aurora-and-documentdb-certificates/
2. https://aws.amazon.com/blogs/database/amazon-rds-customers-update-your-ssl-tls-certificates-by-february-5-2020/
3. https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.SSL-certificate-rotation.html
4. Download the rds-ca-2019-root.pem https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.SSL.html

> Between February 5 and March 5, 2020, RDS will stage the new certificates on your database hosts without restarting
your databases. The certificates will take effect at your next database restart. If you haven’t updated your
application trust stores, your applications will lose connectivity when your database restarts. A restart can occur
because of a planned maintenance action requiring a restart or because of an unplanned restart, such as a database
crash. [2]