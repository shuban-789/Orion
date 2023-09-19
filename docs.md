# Configure SSL

- Generate key via openssl
- Use SSLcert and SSLkey attributes from the config file

# Configuration for /etc/orion/orion.conf

`Allowroot=(yes/no)` - Permit root login or not on RSH server
`BannedUsers=(user1,...,usern)` - Ban the login of these users
`SSLkey=(path/to/file)` - Configure the path to the SSL key
`SSLcert=(path/to/file)` - Configure the path to the SSL certificate
