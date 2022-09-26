const crypto = require("crypto");

/*
Encryption based on aes-256-cbc algorithm
This is made to be compatible with node "createCipheriv.py"
The returned crypto is a hex to allow it to be used in links etc
*/

const initVector = "1234567890123456"; // 16 digits
const Securitykey = "12345678901234567890123456789012"; // must be 32 digits
const algorithm = "aes-256-cbc";

const crypt = {
  async hashCode(password) {
    const cipher = crypto.createCipheriv(algorithm, Securitykey, initVector);
    let encryptedData = cipher.update(password, "utf-8", "hex");
    encryptedData += cipher.final("hex");

    return encryptedData;
  },

  async deHashCode(encryptedData) {
    const decipher = crypto.createDecipheriv(
      algorithm,
      Securitykey,
      initVector
    );

    try {
      let decryptedData = decipher.update(encryptedData, "hex", "utf-8");
      decryptedData += decipher.final("utf8");
      return decryptedData;
    } catch (e) {
      return false;
    }
  },
};

module.exports = crypt;
