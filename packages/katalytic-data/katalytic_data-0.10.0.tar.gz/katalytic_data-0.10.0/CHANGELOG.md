## 0.10.0 (2023-06-26)
### feat
- [[`6dff7d9`](https://gitlab.com/katalytic/katalytic-data/commit/6dff7d91bf0fdb93128cac275aedc704705b8eb4)] add empty_ok=True to as_list_of_lists, as_list_of_dicts, and as_dict_of_lists
- [[`47e1c02`](https://gitlab.com/katalytic/katalytic-data/commit/47e1c02d3741ca27586f11334b9f16d6b59eda62)] add empty_ok=True to is_dict_of_sequences and is_dict_of_sequences_uniform
- [[`9940b28`](https://gitlab.com/katalytic/katalytic-data/commit/9940b28d020444520af39b7499ed7627d62b1cff)] add empty_ok=True to is_sequence_of_dicts and is_sequence_of_dicts_uniform
- [[`d416d01`](https://gitlab.com/katalytic/katalytic-data/commit/d416d01f2c1f9a8700ee32f70556befc89524534)] add empty_ok=True to is_sequence_of_sequences and is_sequence_of_sequences_uniform
- [[`1017718`](https://gitlab.com/katalytic/katalytic-data/commit/1017718e1ceb603240d64db688b257dde464db0d)] add type check for empty_ok
### fix
- [[`72dd27f`](https://gitlab.com/katalytic/katalytic-data/commit/72dd27fce8eec63841bf414f60ff2ef041bdf462)] importlib.metadata.PackageNotFoundError: __init__


## 0.9.2 (2023-05-22)
### fix
- [[`be05243`](https://gitlab.com/katalytic/katalytic-data/commit/be0524340348c5424c99d1e205eac3c5714f164f)] get_version() raises error when running doctest
### refactor
- [[`080d2d8`](https://gitlab.com/katalytic/katalytic-data/commit/080d2d88ee69534e65da316cd9485f36afd2e0d6)] rename "key" parameter to "condition"


## 0.9.1 (2023-05-20)
### fix
- [[`131e3ad`](https://gitlab.com/katalytic/katalytic-data/commit/131e3ad13db07a9e23e33e8d9c66df73a65a95f0)] use `[True, False]` instead of just `False` in the `_types` dict


## 0.9.0 (2023-05-06)
### feat
- [[`1fddfe3`](https://gitlab.com/katalytic/katalytic-data/commit/1fddfe3b1910d55350c004003c808536f4999548)] pop_{min, max}, pop_{min, max}_by_dict_{keys,values}, swap_keys_and_values
### fix
- [[`75403ec`](https://gitlab.com/katalytic/katalytic-data/commit/75403ecb6d65ee217788438530d2ff666dc573cf)] exclude map from all_types_besides('iterables') and correct all_types('dict')


## 0.8.0 (2023-05-05)
### feat
- [[`ae032f2`](https://gitlab.com/katalytic/katalytic-data/commit/ae032f23cf8e387387833a0648184ca6095bf9ed)] move katalytic-checks code into this repo
### fix
- [[`ddc044f`](https://gitlab.com/katalytic/katalytic-data/commit/ddc044f3bdf1a872306cfbb090843e220d7222f5)] all_types()


## 0.7.1 (2023-04-30)
### fix
- [[`5a06ff8`](https://gitlab.com/katalytic/katalytic-data/commit/5a06ff8ee54e58e502c18fee5723bad8c4bf702a)] add missing categories of types and extend the tests


## 0.7.0 (2023-04-30)
### feat
- [[`46caaef`](https://gitlab.com/katalytic/katalytic-data/commit/46caaeff90e1c3bff58e0db81bc082632c0f52a3)] allow passing a str to all_types() and all_types_besides()


## 0.6.0 (2023-04-29)
### feat
- [[`52b8faf`](https://gitlab.com/katalytic/katalytic-data/commit/52b8faf9d53af06a791c4fab8c7b8a70001c1490)] **all_types_besides:** add "numbers" category
- [[`c7c80ad`](https://gitlab.com/katalytic/katalytic-data/commit/c7c80ade75dfa858022855df849c6be6ccb3c4fc)] add all_types


## 0.5.1 (2023-04-29)
### fix
- [[`1f727b0`](https://gitlab.com/katalytic/katalytic-data/commit/1f727b046ec1f5b38608139a2d3b20b363a58720)] **all_types_besides:** add "class" to the "callables" category


## 0.5.0 (2023-04-29)
### feat
- [[`27102cf`](https://gitlab.com/katalytic/katalytic-data/commit/27102cf2a974a2ae73e56afafab38eb66098940c)] **all_types_besides:** add "callables" category
- [[`39cccc6`](https://gitlab.com/katalytic/katalytic-data/commit/39cccc664bd062e73fe80d63a21dedc8cffcb2d2)] add all_types_besides, flatten, flatten_recursive
- [[`12706e2`](https://gitlab.com/katalytic/katalytic-data/commit/12706e2e40dc3127ca680c7121dd720e849d3fdc)] add are_equal
- [[`fbe876b`](https://gitlab.com/katalytic/katalytic-data/commit/fbe876b80301be2ae917b93ee31954d576477af8)] add as_dict_of_lists(), and fix bugs in as_sequence_of_dicts() and as_sequence_of_sequences()
- [[`2a4ac90`](https://gitlab.com/katalytic/katalytic-data/commit/2a4ac90ff94ced5ddbafc6d083d08a3720fb389c)] add as_sequence_of_dicts()
- [[`ed4689c`](https://gitlab.com/katalytic/katalytic-data/commit/ed4689c231abf872c6f3fa130a286105548e69b1)] add as_sequence_of_sequences()
- [[`f1222bf`](https://gitlab.com/katalytic/katalytic-data/commit/f1222bf4b6e54fe5361ad36a49534b1966a837b8)] add contains_all_of, contains_any_of, contains_none_of
- [[`e17e02e`](https://gitlab.com/katalytic/katalytic-data/commit/e17e02e93bbc39c261a92c192fd1755d05a08873)] add detect_fronts, detect_fronts_positive, detect_fronts_negative
- [[`32afee3`](https://gitlab.com/katalytic/katalytic-data/commit/32afee339e97a4dcb0238e76529ab26265f34db8)] add dicts_share_key_order() and dicts_share_value_order()
- [[`a4f833b`](https://gitlab.com/katalytic/katalytic-data/commit/a4f833b15909de35a0940ea5e0656507e046218d)] add first_with_idx(), last_with_idx()
- [[`1caaaba`](https://gitlab.com/katalytic/katalytic-data/commit/1caaaba0678f58725644736ec303385cfdc4fe70)] add is_any_of(), is_none_of()
- [[`7b9b1b5`](https://gitlab.com/katalytic/katalytic-data/commit/7b9b1b55acde94f250399a42c01447bd787c7b5b)] add is_generator
- [[`9caa741`](https://gitlab.com/katalytic/katalytic-data/commit/9caa741e7e273451e37cf2ee32cf1f25d3fa5c48)] add is_sequence() and is_sequence_or_str()
- [[`d3fdf95`](https://gitlab.com/katalytic/katalytic-data/commit/d3fdf9576ff12bd3a717b2f393e4f24996c0bc2f)] add is_sequence_of_sequences(), is_sequence_of_dicts(), and is_dict_of_sequences()
- [[`9a59d37`](https://gitlab.com/katalytic/katalytic-data/commit/9a59d37ee15047ddc250c55a2faaa2a577976dfa)] add is_sequence_of_sequences_uniform(), is_sequence_of_dicts_uniform(), is_dict_of_sequences_uniform()
- [[`563dc12`](https://gitlab.com/katalytic/katalytic-data/commit/563dc12952da62e486efc769a68f4103a2dd55ee)] add is_singleton()
- [[`eeee05f`](https://gitlab.com/katalytic/katalytic-data/commit/eeee05fba6ae67ab439fa4030a1fd1a3901d41a3)] add one(), first(), last()
- [[`5183859`](https://gitlab.com/katalytic/katalytic-data/commit/51838594613e4f47e34a91be19cf16fbef22dc2f)] add pick_all, pick_all_besides, pick_any,
- [[`53cbf04`](https://gitlab.com/katalytic/katalytic-data/commit/53cbf0432bddac3f958be2c068a3d80e4a68e259)] add recursive_map(), sort_dict_by_keys_recursive()
- [[`03767ca`](https://gitlab.com/katalytic/katalytic-data/commit/03767cac16935efbc459567f412a9d382d1a72d8)] add sort_dict_by_values_recursive()
- [[`00d7045`](https://gitlab.com/katalytic/katalytic-data/commit/00d70456642dbfc4ecd7b32269a513dd6660723a)] add sort_recursive
- [[`cb3b145`](https://gitlab.com/katalytic/katalytic-data/commit/cb3b145c1a7c08a6877744693690a981d7475691)] add xor, xor_with_idx
- [[`5d107d9`](https://gitlab.com/katalytic/katalytic-data/commit/5d107d92b115a053b26d7a21aaddb623d4b1057d)] delete checks.py and tests. They were moved to katalytic-checks
- [[`0b9be79`](https://gitlab.com/katalytic/katalytic-data/commit/0b9be79523d7fcdab4f93055ae9b8f0c56f1e595)] remove is_collection() and add is_iterable(), is_iterable_or_str(), is_iterator()
- [[`d8d64aa`](https://gitlab.com/katalytic/katalytic-data/commit/d8d64aa37c1926303bc4f618bd0bd0fec23b5db4)] update as_sequence_of_dicts()
### fix
- [[`a59bed1`](https://gitlab.com/katalytic/katalytic-data/commit/a59bed13380f4e1633e0515d4195361d6e4da7c8)] ImportError
- [[`322a828`](https://gitlab.com/katalytic/katalytic-data/commit/322a82884728ae61ffc3b7bf88f2b2d801c6f197)] add missing import, use the correct kw arg
- [[`7640b61`](https://gitlab.com/katalytic/katalytic-data/commit/7640b6192a19e0d2e2af8ea0e929ffe0d1e52daf)] dicts_share_value_order(), dicts_share_key_order()
- [[`120950e`](https://gitlab.com/katalytic/katalytic-data/commit/120950ec78b1b2eba9535d06948b23bfa84a1593)] don't let python mix bools with 0 and 1
- [[`e7f8161`](https://gitlab.com/katalytic/katalytic-data/commit/e7f81615643230c1384bea6cb8981d92898879cc)] release
- [[`d25b099`](https://gitlab.com/katalytic/katalytic-data/commit/d25b09959d1a925d28399bc79f2644f2c6d197a7)] release
- [[`a5944c0`](https://gitlab.com/katalytic/katalytic-data/commit/a5944c0bfa31e99e702333dd0862909b17a982a0)] release
- [[`c05c712`](https://gitlab.com/katalytic/katalytic-data/commit/c05c71281084d8cbbba465415c88df689dd5d799)] release
- [[`6b7ed67`](https://gitlab.com/katalytic/katalytic-data/commit/6b7ed670100f50728c00b6971137735ca0214221)] release
- [[`11c54be`](https://gitlab.com/katalytic/katalytic-data/commit/11c54be3978ee6c2e1b8ef7f3f56802e2e631a69)] release
- [[`122ece9`](https://gitlab.com/katalytic/katalytic-data/commit/122ece923011ab96e10023bae5a602b90025158b)] release
- [[`6b7063f`](https://gitlab.com/katalytic/katalytic-data/commit/6b7063f694840f33f09a0ffd461a9868f365e03d)] release
- [[`7bf31c7`](https://gitlab.com/katalytic/katalytic-data/commit/7bf31c71305029695de0a90f3546941863c98717)] release
- [[`d377401`](https://gitlab.com/katalytic/katalytic-data/commit/d377401a2afb57ea1fe6270b27e01d50340175b8)] release
- [[`cc167ec`](https://gitlab.com/katalytic/katalytic-data/commit/cc167ec169dbba15a46ba6ec1d39b99c673923f9)] release
- [[`b144802`](https://gitlab.com/katalytic/katalytic-data/commit/b144802676ef160d297aa7b004a00d428f39fc1f)] rename recursive_map() -> map_recursive()
- [[`15daadf`](https://gitlab.com/katalytic/katalytic-data/commit/15daadfc274b7de627a656dae8771ec5a7088662)] rename recursive_map() -> map_recursive()
- [[`163f359`](https://gitlab.com/katalytic/katalytic-data/commit/163f359ada349a4cbcec44f1358dff2cf003b66c)] replace True with bool in map
### refactor
- [[`b45f8c9`](https://gitlab.com/katalytic/katalytic-data/commit/b45f8c98fce269e9d4111b0e5f1381d3d7268fef)] call is_singleton()
- [[`1eabb04`](https://gitlab.com/katalytic/katalytic-data/commit/1eabb045ba4ade3af6bfd54140e3f0e59ca81aad)] change arg names
- [[`8293f3e`](https://gitlab.com/katalytic/katalytic-data/commit/8293f3ef6d8fd58b20e92791f5bb7a518e97a429)] is_iterable
- [[`4bad63c`](https://gitlab.com/katalytic/katalytic-data/commit/4bad63ca2bda10e41de30d6a1964f867cf395419)] rename are_equal to is_equal
- [[`7d18c52`](https://gitlab.com/katalytic/katalytic-data/commit/7d18c529cc3db93717a00778e5fe488ff4fe3b7f)] rename are_equal to is_equal
- [[`416e795`](https://gitlab.com/katalytic/katalytic-data/commit/416e7954e03f762ada53283c93f4f71dd7fa2ea9)] reposition a Test class
- [[`e3fd9fe`](https://gitlab.com/katalytic/katalytic-data/commit/e3fd9feeb976e2cde6b5e5308a99a00e31ffe8cd)] simplify is_any_of


## 0.3.0 (2023-04-26)
### feat
- [[`39cccc6`](https://gitlab.com/katalytic/katalytic-data/commit/39cccc664bd062e73fe80d63a21dedc8cffcb2d2)] add all_types_besides, flatten, flatten_recursive
- [[`fbe876b`](https://gitlab.com/katalytic/katalytic-data/commit/fbe876b80301be2ae917b93ee31954d576477af8)] add as_dict_of_lists(), and fix bugs in as_sequence_of_dicts() and as_sequence_of_sequences()
- [[`2a4ac90`](https://gitlab.com/katalytic/katalytic-data/commit/2a4ac90ff94ced5ddbafc6d083d08a3720fb389c)] add as_sequence_of_dicts()
- [[`ed4689c`](https://gitlab.com/katalytic/katalytic-data/commit/ed4689c231abf872c6f3fa130a286105548e69b1)] add as_sequence_of_sequences()
- [[`e17e02e`](https://gitlab.com/katalytic/katalytic-data/commit/e17e02e93bbc39c261a92c192fd1755d05a08873)] add detect_fronts, detect_fronts_positive, detect_fronts_negative
- [[`a4f833b`](https://gitlab.com/katalytic/katalytic-data/commit/a4f833b15909de35a0940ea5e0656507e046218d)] add first_with_idx(), last_with_idx()
- [[`eeee05f`](https://gitlab.com/katalytic/katalytic-data/commit/eeee05fba6ae67ab439fa4030a1fd1a3901d41a3)] add one(), first(), last()
- [[`5183859`](https://gitlab.com/katalytic/katalytic-data/commit/51838594613e4f47e34a91be19cf16fbef22dc2f)] add pick_all, pick_all_besides, pick_any,
- [[`53cbf04`](https://gitlab.com/katalytic/katalytic-data/commit/53cbf0432bddac3f958be2c068a3d80e4a68e259)] add recursive_map(), sort_dict_by_keys_recursive()
- [[`03767ca`](https://gitlab.com/katalytic/katalytic-data/commit/03767cac16935efbc459567f412a9d382d1a72d8)] add sort_dict_by_values_recursive()
- [[`00d7045`](https://gitlab.com/katalytic/katalytic-data/commit/00d70456642dbfc4ecd7b32269a513dd6660723a)] add sort_recursive
- [[`cb3b145`](https://gitlab.com/katalytic/katalytic-data/commit/cb3b145c1a7c08a6877744693690a981d7475691)] add xor, xor_with_idx
- [[`d8d64aa`](https://gitlab.com/katalytic/katalytic-data/commit/d8d64aa37c1926303bc4f618bd0bd0fec23b5db4)] update as_sequence_of_dicts()
### fix
- [[`a59bed1`](https://gitlab.com/katalytic/katalytic-data/commit/a59bed13380f4e1633e0515d4195361d6e4da7c8)] ImportError
- [[`322a828`](https://gitlab.com/katalytic/katalytic-data/commit/322a82884728ae61ffc3b7bf88f2b2d801c6f197)] add missing import, use the correct kw arg
- [[`120950e`](https://gitlab.com/katalytic/katalytic-data/commit/120950ec78b1b2eba9535d06948b23bfa84a1593)] don't let python mix bools with 0 and 1
- [[`b144802`](https://gitlab.com/katalytic/katalytic-data/commit/b144802676ef160d297aa7b004a00d428f39fc1f)] rename recursive_map() -> map_recursive()
- [[`15daadf`](https://gitlab.com/katalytic/katalytic-data/commit/15daadfc274b7de627a656dae8771ec5a7088662)] rename recursive_map() -> map_recursive()
- [[`163f359`](https://gitlab.com/katalytic/katalytic-data/commit/163f359ada349a4cbcec44f1358dff2cf003b66c)] replace True with bool in map
### refactor
- [[`b45f8c9`](https://gitlab.com/katalytic/katalytic-data/commit/b45f8c98fce269e9d4111b0e5f1381d3d7268fef)] call is_singleton()
- [[`1eabb04`](https://gitlab.com/katalytic/katalytic-data/commit/1eabb045ba4ade3af6bfd54140e3f0e59ca81aad)] change arg names
- [[`4bad63c`](https://gitlab.com/katalytic/katalytic-data/commit/4bad63ca2bda10e41de30d6a1964f867cf395419)] rename are_equal to is_equal
- [[`7d18c52`](https://gitlab.com/katalytic/katalytic-data/commit/7d18c529cc3db93717a00778e5fe488ff4fe3b7f)] rename are_equal to is_equal
- [[`416e795`](https://gitlab.com/katalytic/katalytic-data/commit/416e7954e03f762ada53283c93f4f71dd7fa2ea9)] reposition a Test class
- [[`e3fd9fe`](https://gitlab.com/katalytic/katalytic-data/commit/e3fd9feeb976e2cde6b5e5308a99a00e31ffe8cd)] simplify is_any_of


## 0.1.1 (2023-04-16)
## Fix
* nothing


## 0.1.0 (2023-04-16)
### Feature
* Add is_collection() ([`bf29261`](https://github.com/katalytic/katalytic-data/commit/bf2926172f56d000d1f09318ab212c7b9747a8b0))
* Add is_primitive() ([`ed950cc`](https://github.com/katalytic/katalytic-data/commit/ed950ccdd8e4cd4d4439cb0ab9c763d55135461d))
* Add sort_dict_by_values() ([`6b3c985`](https://github.com/katalytic/katalytic-data/commit/6b3c9856c69e088467087345743a38e6294def7a))
* Add sort_dict_by_keys() ([`5c05e48`](https://github.com/katalytic/katalytic-data/commit/5c05e48c4cc8afaf6a861103784690ebc153dcc8))
* Add map_dict_values() ([`ba289c5`](https://github.com/katalytic/katalytic-data/commit/ba289c5f5cb21ff66d89bb833f30e2be678e15da))
* Add map_dict_keys() ([`f6b1410`](https://github.com/katalytic/katalytic-data/commit/f6b141050b901456041bf049dc3b329c2d8fcec8))
