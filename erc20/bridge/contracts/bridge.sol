pragma solidity ^0.4.15;

library Authorities {
    function contains (address[] self, address value) internal pure returns (bool) {
        for (uint i = 0; i < self.length; i++) {
            if (self[i] == value) {
                return true;
            }
        }
        return false;
    }
}

/// Library used only to test Signer library via rpc calls
library SignerTest {
    function signer (bytes signature, bytes message) public pure returns (address) {
        return Signer.signer(signature, message);
    }
}

library Utils {
    function toString (uint256 v) internal pure returns (string str) {
        // it is used only for small numbers
        bytes memory reversed = new bytes(8);
        uint i = 0;
        while (v != 0) {
            uint remainder = v % 10;
            v = v / 10;
            reversed[i++] = byte(48 + remainder);
        }
        bytes memory s = new bytes(i);
        for (uint j = 0; j < i; j++) {
            s[j] = reversed[i - j - 1];
        }
        str = string(s);
    }
}

library Signer {
    function signer (bytes signature, bytes message) internal pure returns (address) {
        require(signature.length == 65);
        bytes32 r;
        bytes32 s;
        bytes1 v;
        // solium-disable-next-line security/no-inline-assembly
        assembly {
            r := mload(add(signature, 0x20))
            s := mload(add(signature, 0x40))
            v := mload(add(signature, 0x60))
        }
        return ecrecover(hash(message), uint8(v), r, s);
    }

    function hash (bytes message) internal pure returns (bytes32) {
        bytes memory prefix = "\x19Ethereum Signed Message:\n";
        return keccak256(prefix, Utils.toString(message.length), message);
    }
}

contract HomeBridge {
    using Authorities for address[];

    /// Number of authorities signatures required to withdraw the money.
    ///
    /// Must be lesser than number of authorities.
    uint public requiredSignatures;

    /// Contract authorities.
    address[] public authorities;

    /// Used foreign transaction hashes.
    mapping (bytes32 => bool) withdraws;

    /// Event created on money deposit.
    event Deposit (address recipient, uint value);

    /// Event created on money withdraw.
    event Withdraw (address recipient, uint value);

    /// Multisig authority validation
    modifier allAuthorities (uint8[] v, bytes32[] r, bytes32[] s, bytes message) {
        var hash = Signer.hash(message);
        var used = new address[](requiredSignatures);

        require(requiredSignatures <= v.length);

        for (uint i = 0; i < requiredSignatures; i++) {
            var a = ecrecover(hash, v[i], r[i], s[i]);
            require(authorities.contains(a));
            require(!used.contains(a));
            used[i] = a;
        }
        _;
    }

    /// Constructor.
    function HomeBridge (uint n, address[] a) public {
        require(n != 0);
        require(n <= a.length);
        requiredSignatures = n;
        authorities = a;
    }

    /// Should be used to deposit money.
    function () public payable {
        Deposit(msg.sender, msg.value);
    }

    /// Used to withdraw money from the contract.
    ///
    /// message contains:
    /// withdrawal recipient (bytes20)
    /// withdrawal value (uint)
    /// foreign transaction hash (bytes32) // to avoid transaction duplication
    ///
    /// NOTE that anyone can call withdraw provided they have the
    /// message and required signatures!
    function withdraw (uint8[] v, bytes32[] r, bytes32[] s, bytes message) public allAuthorities(v, r, s, message) {
        require(message.length == 84);
        address recipient;
        uint value;
        bytes32 hash;
        // solium-disable-next-line security/no-inline-assembly
        assembly {
            // layout of message :: bytes:
            // offset  0: 32 bytes :: uint (little endian) - message length
            // offset 32: 20 bytes :: address - recipient address
            // offset 52: 32 bytes :: uint (little endian) - value
            // offset 84: 32 bytes :: bytes32 - transaction hash

            // we require above that message length == 84.
            // bytes 1 to 32 are 0 because message length is stored as little endian.
            // mload always reads 32 bytes.
            // so we can and have to start reading recipient at offset 20 instead of 32.
            // if we were to read at 32 the address would contain part of value and be corrupted.
            // when reading from offset 20 mload will read 12 zero bytes followed
            // by the 20 recipient address bytes and correctly convert it into an address.
            // this saves some storage/gas over the alternative solution
            // which is padding address to 32 bytes and reading recipient at offset 32.
            // for more details see discussion in:
            // https://github.com/paritytech/parity-bridge/issues/61
            recipient := mload(add(message, 20))
            value := mload(add(message, 52))
            hash := mload(add(message, 84))
        }

        // Duplicated withdraw
        require(!withdraws[hash]);

        // Order of operations below is critical to avoid TheDAO-like bug
        withdraws[hash] = true;
        recipient.transfer(value);
        Withdraw(recipient, value);
    }
}

contract ERC20 {
    function transfer(address to, uint256 value) public returns (bool);
    function transferFrom(address from, address to, uint256 value) public returns (bool);
    function allowance(address owner, address spender) public constant returns (uint256);
}

contract ForeignBridge {
    using Authorities for address[];

    struct SignaturesCollection {
        /// Signed message.
        bytes message;
        /// Authorities who signed the message.
        address[] signed;
        /// Signaturs
        bytes[] signatures;
    }

    /// Number of authorities signatures required to withdraw the money.
    ///
    /// Must be lesser than number of authorities.
    uint public requiredSignatures;

    /// Contract authorities.
    address[] public authorities;

    /// Pending deposits and authorities who confirmed them
    mapping (bytes32 => address[]) deposits;

    /// List of authorities confirmed to set up ERC-20 token address
    mapping (address => address[]) public token_address;
    
    /// Token to work with
    ERC20 public erc20token;
    
    /// Event created when new token address is set up.
    event TokenAddress(address token);
    
    /// Pending signatures and authorities who confirmed them
    mapping (bytes32 => SignaturesCollection) signatures;

    /// Event created on money deposit.
    event Deposit(address recipient, uint value);

    /// Event created on money withdraw.
    event Withdraw(address recipient, uint value);

    /// Collected signatures which should be relayed to home chain.
    event CollectedSignatures(address authority, bytes32 messageHash);

    /// Constructor.
    function ForeignBridge(uint n, address[] a) public {
        require(n != 0);
        require(n <= a.length);
        requiredSignatures = n;
        authorities = a;
    }

    /// Multisig authority validation
    modifier onlyAuthority () {
        require(authorities.contains(msg.sender));
        _;
    }

    /// Set up the token address.
    ///
    /// token address (address)
    function setTokenAddress (ERC20 token) public onlyAuthority() {
        // Protect duplicated request
        require(!token_address[token].contains(msg.sender));

        token_address[token].push(msg.sender);
        // TODO: this may cause troubles if requriedSignatures len is changed
        if (token_address[token].length == requiredSignatures) {
            erc20token = ERC20(token);
            TokenAddress(token);
        }
    }

    /// Used to deposit money to the contract.
    ///
    /// deposit recipient (bytes20)
    /// deposit value (uint)
    /// mainnet transaction hash (bytes32) // to avoid transaction duplication
    function deposit (address recipient, uint value, bytes32 transactionHash) public onlyAuthority() {
        // Protection from misbehaing authority
        var hash = keccak256(recipient, value, transactionHash);

        // Duplicated deposits
        require(!deposits[hash].contains(msg.sender));

        deposits[hash].push(msg.sender);
        // TODO: this may cause troubles if requriedSignatures len is changed
        if (deposits[hash].length == requiredSignatures) {
            erc20token.transfer(recipient, value);
            Deposit(recipient, value);
        }
    }

    /// To swap token to money the account must allow this explicitly
    /// in the token contract by calling approveAndCall with address
    /// of the bridge account.
    function receiveApproval(address _from, uint256 _value, address _tokenContract, bytes _msg) external returns(bool) {
        require(msg.sender == address(erc20token)); 
        require(erc20token.allowance(_from, this) >= _value); 
        erc20token.transferFrom(_from, this, _value);
        Withdraw(_from, _value);
        
        return true;
    }

    /// Should be used as sync tool
    ///
    /// Message is a message that should be relayed to main chain once authorities sign it.
    ///
    /// for withdraw message contains:
    /// withdrawal recipient (bytes20)
    /// withdrawal value (uint)
    /// foreign transaction hash (bytes32) // to avoid transaction duplication
    function submitSignature (bytes signature, bytes message) public onlyAuthority() {
        // Validate submited signatures
        require(Signer.signer(signature, message) == msg.sender);

        // Valid withdraw message must have 84 bytes
        require(message.length == 84);
        var hash = keccak256(message);

        // Duplicated signatures
        require(!signatures[hash].signed.contains(msg.sender));
        signatures[hash].message = message;
        signatures[hash].signed.push(msg.sender);
        signatures[hash].signatures.push(signature);

        // TODO: this may cause troubles if requiredSignatures len is changed
        if (signatures[hash].signed.length == requiredSignatures) {
            CollectedSignatures(msg.sender, hash);
        }
    }

    /// Get signature
    function signature (bytes32 hash, uint index) public view returns (bytes) {
        return signatures[hash].signatures[index];
    }

    /// Get message
    function message (bytes32 hash) public view returns (bytes) {
        return signatures[hash].message;
    }
}
