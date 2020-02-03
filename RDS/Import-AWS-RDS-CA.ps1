# See https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.SSL.html
# rds-combined-ca-bundle.p7b includes both the intermediate and root (both rds-ca-2015-root and rds-ca-2019-root)
# certificates.
"Download rds certificate bundle"
Invoke-WebRequest -Uri https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.p7b -OutFile 'rds-combined-ca-bundle.p7b'

"Import rds certificate bundle"
Import-Certificate –FilePath rds-combined-ca-bundle.p7b –CertStorelocation Cert:\LocalMachine\Root
