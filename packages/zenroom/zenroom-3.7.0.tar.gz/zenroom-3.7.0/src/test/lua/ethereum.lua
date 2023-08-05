-- Some tests with Ethereum

local ETH = require('crypto_ethereum')
-- the transaction I want to encode is (e.g.)
-- | nonce     |                                          0 |
-- | gas price |                                          0 |
-- | gas limit |                                      25000 |
-- | to        | 0x627306090abaB3A6e1400e9345bC60c78a8BEf57 |
-- | value     |                                         11 |
-- | data      |                                            |
-- | chainId   |                                       1337 |

-- start Besu with the following command
-- besu --network=dev --miner-enabled --miner-coinbase=0xfe3b557e8fb62b89f4916b721be55ceb828dbd73 --rpc-http-cors-origins="all" --host-allowlist="*" --rpc-ws-enabled --rpc-http-enabled --data-path=/tmp/tmpDatdir

-- 0 is encoded as the empty octet (O.new())
local fields = {"nonce", "gas_price", "gas_limit", "to",
		"value", "data"}
local tx = {}
tx["nonce"] = ETH.o2n(O.new())
tx["gas_price"] = INT.new(1000)
tx["gas_limit"] = INT.new(25000)
tx["to"] = O.from_hex('627306090abaB3A6e1400e9345bC60c78a8BEf57')
tx["value"] = INT.new(O.from_hex('11'))
tx["data"] = O.new()

for i=1,100 do
   -- this are overwritten during encoding, so we need to set them each time
   -- v contains the chain id (when the transaction is not signed)
   -- We always use the chain id
   tx["v"] = INT.new(1337)
   tx["r"] = O.new()
   tx["s"] = O.new()
   local from = O.random(32)
   local pk = ECDH.pubgen(from)
   local add = ETH.address_from_public_key(pk)
   local not_add = sha256(add):sub(13, 32)

   local encodedTx = ETH.encodeSignedTransaction(from, tx)

   local decodedTx = ETH.decodeTransaction(encodedTx)

   for _, v in pairs(fields) do
      assert(tx[v] == decodedTx[v])
   end
   assert(ETH.verifySignatureTransaction(pk, tx),
	  "verification from pk and tx failed")
   assert(ETH.verifySignatureTransaction(pk, decodedTx),
	  "verification from pk and decodedTx failed")
   assert(ETH.verify_transaction_from_address(add, tx),
	  "verification from add and tx failed")
   assert(ETH.verify_transaction_from_address(add, decodedTx),
	  "verification from add and decodedTx failed")
   assert(not ETH.verify_transaction_from_address(not_add, decodedTx),
	  "verification from not_add and decodedTx succeded")
end

assert(ETH.make_storage_data(O.from_string('ciao mondo')) == O.from_hex('b374012b0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000a6369616f206d6f6e646f00000000000000000000000000000000000000000000'))
assert(ETH.make_storage_data(O.from_string('aaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddaaaabbbbccccddddpadding')) == O.from_hex('b374012b00000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000207616161616262626263636363646464646161616162626262636363636464646461616161626262626363636364646464616161616262626263636363646464646161616162626262636363636464646461616161626262626363636364646464616161616262626263636363646464646161616162626262636363636464646461616161626262626363636364646464616161616262626263636363646464646161616162626262636363636464646461616161626262626363636364646464616161616262626263636363646464646161616162626262636363636464646461616161626262626363636364646464616161616262626263636363646464646161616162626262636363636464646461616161626262626363636364646464616161616262626263636363646464646161616162626262636363636464646461616161626262626363636364646464616161616262626263636363646464646161616162626262636363636464646461616161626262626363636364646464616161616262626263636363646464646161616162626262636363636464646461616161626262626363636364646464616161616262626263636363646464646161616162626262636363636464646461616161626262626363636364646464616161616262626263636363646464646161616162626262636363636464646470616464696e6700000000000000000000000000000000000000000000000000'))


-- The following transaction depends on the address of the smart contract
-- tx = {
--    nonce=O.new(),
--    to=O.from_hex('F12b5dd4EAD5F743C6BaA640B0216200e89B60Da'),
--    value=O.new(),
--    data=makeWriteStringData('generated by script'),
--    gasPrice=O.from_hex('03e8'),
--    -- --gasLimit=INT.new('3000000'),
--    gasLimit=O.from_hex('2dc6c0'),
--    v=INT.new(1337),
--    r=O.new(),
--    s=O.new()
-- }

-- encodedTx = encodeSignedTransaction(from, tx)
-- print(encodedTx:hex())

print("New key pair")
local kp = ETH.keygen()
print(kp.address:hex())
print(kp.private:hex())


-- -- Send some eth to the new address
-- tx = {
--    nonce=O.from_hex('01'),
--    to=kp.address,
--    value=O.from_hex('100000'),
--    data=O.new(),
--    gasPrice=O.from_hex('03e8'),
--    -- --gasLimit=INT.new('3000000'),
--    gasLimit=O.from_hex('2dc6c0'),
--    v=INT.new(1337),
--    r=O.new(),
--    s=O.new()
-- }

-- encodedTx = encodeSignedTransaction(from, tx)
-- print("Send some eth to the new address")
-- print(encodedTx:hex())


-- Some test with data generation for smart conctract
print("ERC 20")
assert(ETH.erc20.balanceOf(O.from_hex('19e942FB3193bb2a3D6bAD206ECBe9E60599c388')) == O.from_hex('70a0823100000000000000000000000019e942fb3193bb2a3d6bad206ecbe9e60599c388'))
assert(ETH.erc20.transfer(O.from_hex('e24Cd6B528A513181C765d3dadb0809E1eF991f5'), BIG.from_decimal('1000')) == O.from_hex('a9059cbb000000000000000000000000e24cd6b528a513181c765d3dadb0809e1ef991f500000000000000000000000000000000000000000000000000000000000003e8'))
assert(ETH.erc20.decimals() == O.from_hex('313ce567'))
assert(ETH.erc20.symbol() == O.from_hex('95d89b41'))
assert(ETH.erc20.totalSupply() == O.from_hex('18160ddd'))
assert(ETH.erc20.approve(O.from_hex('19e942FB3193bb2a3D6bAD206ECBe9E60599c388'), 1000) == O.from_hex('095ea7b300000000000000000000000019e942fb3193bb2a3d6bad206ecbe9e60599c38800000000000000000000000000000000000000000000000000000000000003e8'))
assert(ETH.erc20.transferFrom(O.from_hex('19e942FB3193bb2a3D6bAD206ECBe9E60599c388'), O.from_hex('e24Cd6B528A513181C765d3dadb0809E1eF991f5'), 1000) == O.from_hex('23b872dd00000000000000000000000019e942fb3193bb2a3d6bad206ecbe9e60599c388000000000000000000000000e24cd6b528a513181c765d3dadb0809e1ef991f500000000000000000000000000000000000000000000000000000000000003e8'))


-- tx = {}
-- tx["nonce"] = ETH.o2n(O.new())
-- tx["gasPrice"] = INT.new(1000)
-- tx["gasLimit"] = INT.new(25000)
-- tx["to"] = O.from_hex('627306090abaB3A6e1400e9345bC60c78a8BEf57')
-- tx["value"] = INT.new(O.from_hex('11'))
-- tx["data"] = O.new()
-- -- v contains the chain id (when the transaction is not signed)
-- -- We always use the chain id
-- tx["v"] = INT.new(1337)
-- tx["r"] = O.new()
-- tx["s"] = O.new()

-- from = O.from_hex('ae6ae8e5ccbfb04590405997ee2d52d2b330726137b875053c36d94e974d162f')
-- pk = ECDH.pubgen(from)


-- encodedTx = ETH.encodeSignedTransaction(from, tx)

-- print(encodedTx:hex())
-- decodedTx = ETH.decodeTransaction(encodedTx)

example1 = ETH.data_contract_factory('baz', {'uint32', 'bool'})
assert(example1(69, true) == O.from_hex('cdcd77c000000000000000000000000000000000000000000000000000000000000000450000000000000000000000000000000000000000000000000000000000000001'))


example2 = ETH.data_contract_factory('bar', {'bytes3[2]'})
assert(example2({O.from_str('abc'),O.from_str('def')}) == O.from_hex('fce353f661626300000000000000000000000000000000000000000000000000000000006465660000000000000000000000000000000000000000000000000000000000'))

example3 = ETH.data_contract_factory('sam', {'bytes', 'bool', 'uint256[]'})
assert(example3(O.from_str('dave'), true, {1,2,3}) == O.from_hex('a5643bf20000000000000000000000000000000000000000000000000000000000000060000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000000000000000000000000000000000000000000464617665000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000003'))

example4 = ETH.data_contract_factory('f', {'uint256', 'uint32[]', 'bytes10', 'bytes'})
assert(example4(0x123,{0x456, 0x789}, "1234567890", "Hello, world!") == O.from_hex('8be6524600000000000000000000000000000000000000000000000000000000000001230000000000000000000000000000000000000000000000000000000000000080313233343536373839300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000004560000000000000000000000000000000000000000000000000000000000000789000000000000000000000000000000000000000000000000000000000000000d48656c6c6f2c20776f726c642100000000000000000000000000000000000000'))

example5 = ETH.data_contract_factory('pippo', {'string', 'address[]', 'bytes'})
assert(example5("1234567890123456789012345678901234567890", {O.from_hex("d9145CCE52D386f254917e481eB44e9943F39138"), O.from_hex("d9145CCE52D386f254917e481eB44e9943F39138"), O.from_hex("d9145CCE52D386f254917e481eB44e9943F39138")}, O.from_hex("1234567890123456789012345678901234567890")) == O.from_hex('7efcfc8a000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000c000000000000000000000000000000000000000000000000000000000000001400000000000000000000000000000000000000000000000000000000000000028313233343536373839303132333435363738393031323334353637383930313233343536373839300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003000000000000000000000000d9145cce52d386f254917e481eb44e9943f39138000000000000000000000000d9145cce52d386f254917e481eb44e9943f39138000000000000000000000000d9145cce52d386f254917e481eb44e9943f3913800000000000000000000000000000000000000000000000000000000000000141234567890123456789012345678901234567890000000000000000000000000'))

print('-------------------------------------------')
print('Test: checksum_encode')

local test_checksum = {"0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed","0xfB6916095ca1df60bB79Ce92cE3Ea74c37c5d359","0xdbF03B407c01E7cD3CBea99509d93f8DDDC8C6FB","0xD1220A0cf47c7B9Be7A2E6BA89F429762e7b9aDb", "0x52908400098527886E0F7030069857D2E4169EE7", "0x8617E340B3D01FA5F11F306F4090FD50E238070D", "0xde709f2102306220921060314715629080e2fb77", "0x27b1fdb04752bbc536007a920d24acb045561c26"}
local test_wrong_check = {"0x5AAeb6053F3E94C9b9A09f33669435E7Ef1BeAed","0xfB6916095ca1df60bb79Ce92cE3Ea74c37c5d359"}
for i, v in pairs(test_checksum) do
    print("Test case "..i)
    local addr_bytes = O.from_hex(v)
    local checksum_encoded = ETH.checksum_encode(addr_bytes)
    assert(checksum_encoded == v, "Wrong checksum encoding")
end

print('Test: checksum_encode failure')
for i, v in pairs(test_wrong_check) do
    print("Test case "..i)
    local addr_bytes = O.from_hex(v)
    local checksum_encoded = ETH.checksum_encode(addr_bytes)
    assert(checksum_encoded ~= v, "Wrong checksum encoding")
end
