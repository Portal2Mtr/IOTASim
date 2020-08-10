import iota
from pprint import pprint
from pow import ccurl_interface

# Generate seed
myseed = iota.crypto.types.Seed.random()

# Generate two addresses
addres_generator = iota.crypto.addresses.AddressGenerator(myseed)
addys = addres_generator.get_addresses(1, count=2)

# Preparing transactions
pt = iota.ProposedTransaction(address = iota.Address(addys[0]),
                              tag     = iota.Tag(b'LOCALATTACHINTERFACE99999'),
                              value   = 0)

pt2 = iota.ProposedTransaction(address = iota.Address(addys[1]),
                               tag     = iota.Tag(b'LOCALATTACHINTERFACE99999'),
                               value   = 0)

# Preparing bundle that consists of both transactions prepared in the previous example
pb = iota.ProposedBundle(transactions=[pt2,pt])

# Generate bundle hash
pb.finalize()

# Declare an api instance
api = iota.Iota("https://nodes.thetangle.org:443")

# Get tips to be approved by your bundle
gta = api.get_transactions_to_approve(depth=3) # Depth = how many milestones back

minimum_weight_magnitude = 14 # target is mainnet

# perform PoW locally
bundle_trytes =\
    ccurl_interface.attach_to_tangle(
        pb.as_tryte_strings(),
        gta['trunkTransaction'],
        gta['branchTransaction'],
        minimum_weight_magnitude
    )

# Broadcast transactions on the Tangle
broadcasted = api.broadcast_and_store(bundle_trytes)

# Returned transactions, can be stored...

bundle_broadcasted =iota.Bundle.from_tryte_strings(broadcasted['trytes'])

pprint('Local pow broadcasted transactions are:')
pprint(bundle_broadcasted.as_json_compatible())
