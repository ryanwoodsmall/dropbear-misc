// XXX - please do not remove any occurrence of "/current/" below
// XXX - it is `sed -i`-ed out in the RPM spec but used in crosware
#define DROPBEAR_DEFPORT "2222"
#define DSS_PRIV_FILENAME "/opt/dropbear/etc/dropbear_dss_host_key"
#define RSA_PRIV_FILENAME "/opt/dropbear/etc/dropbear_rsa_host_key"
#define ECDSA_PRIV_FILENAME "/opt/dropbear/etc/dropbear_ecdsa_host_key"
#define ED25519_PRIV_FILENAME "/opt/dropbear/etc/dropbear_ed25519_host_key"
#define DROPBEAR_SMALL_CODE 0
//#define DROPBEAR_BLOWFISH 1
#define DROPBEAR_TWOFISH256 1
#define DROPBEAR_TWOFISH128 1
#define DROPBEAR_3DES 1
#define DROPBEAR_CHACHA20POLY1305 1
#define DROPBEAR_ED25519 1
#define DROPBEAR_ENABLE_CBC_MODE 1
#define DROPBEAR_ENABLE_GCM_MODE 1
#define DROPBEAR_DH_GROUP16 1
#define DROPBEAR_SVR_PASSWORD_AUTH 1
#define DROPBEAR_SVR_PAM_AUTH 0
#define DROPBEAR_SVR_PUBKEY_AUTH 1
#define DROPBEAR_PATH_SSH_PROGRAM "/opt/dropbear/current/bin/dbclient"
#define DROPBEAR_X11FWD 1
#define DROPBEAR_SHA1_96_HMAC 1
#define LOG_COMMANDS 1
#define DEFAULT_KEEPALIVE 30
#define DEFAULT_PATH "/usr/local/bin:/usr/bin:/bin:/opt/dropbear/current/bin"
#define SFTPSERVER_PATH "/usr/libexec/openssh/sftp-server"
//#define DEBUG_TRACE 4
#define DROPBEAR_DH_GROUP1 1
//#define DROPBEAR_DH_GROUP1_CLIENTONLY 0
#define DROPBEAR_DSS 1
#define DROPBEAR_RSA_SHA1 1
#define DROPBEAR_SHA2_512_HMAC 1
//#define DROPBEAR_USE_SSH_CONFIG 1
