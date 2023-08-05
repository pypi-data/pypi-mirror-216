## 0.12.0 (2023-06-26)
### feat
- [[`9eb3bef`](https://gitlab.com/katalytic/katalytic-files/commit/9eb3bef4df0ea6e46ad15dfbbc9fdb8d02910c3f)] add is_file_empty
### fix
- [[`eaa894e`](https://gitlab.com/katalytic/katalytic-files/commit/eaa894e7e49b30dbb5921195bf9360ff71771d88)] **load_csv:** ValueError: invalid literal for int() with base 10: '0.2'
### refactor
- [[`8f3c71c`](https://gitlab.com/katalytic/katalytic-files/commit/8f3c71c064acaa4e508735ffc3515462ee4a873f)] change code order to make the flow more obvious
- [[`0c49c25`](https://gitlab.com/katalytic/katalytic-files/commit/0c49c25c966944f9463d099a2673d9db87ed7b6d)] use errno codes instead of hardcoded numbers


## 0.11.1 (2023-06-02)
### fix
- [[`a4580e6`](https://gitlab.com/katalytic/katalytic-files/commit/a4580e60c9090f424dc5613fac8bdcad9c407a84)] use katalytic.data._UNDEFINED


## 0.11.0 (2023-06-01)
### feat
- [[`16824a0`](https://gitlab.com/katalytic/katalytic-files/commit/16824a05a641d9dc33b4dffbf196844a49fda7dc)] add default parameter to the load functions
- [[`9bc2856`](https://gitlab.com/katalytic/katalytic-files/commit/9bc2856d4ebe4b27eb8b9a22a4a2913ac415f40c)] add default parameter to the load functions


## 0.10.0 (2023-06-01)
### feat
- [[`b2a6c34`](https://gitlab.com/katalytic/katalytic-files/commit/b2a6c345943e9fdb1b2972ca39f7541f5b0dda2d)] add exists and make_dirs parameters to the save_X functions
### fix
- [[`246cce3`](https://gitlab.com/katalytic/katalytic-files/commit/246cce364cf094a57d860c94def8ef7aee0d5bd0)] change {delete,move,copy}_{file,dir} defaults to be more convenient instead of safer
- [[`1cd06f4`](https://gitlab.com/katalytic/katalytic-files/commit/1cd06f420f3aa915b97c0bf752401a347bc4188a)] docstring not being shown for load() and save()
- [[`ff90a28`](https://gitlab.com/katalytic/katalytic-files/commit/ff90a28647d3a5c28b4f0129e19b723d16cb3e06)] make _get_all() and related functions return the same type as the input (str or Path)
- [[`449a83a`](https://gitlab.com/katalytic/katalytic-files/commit/449a83ae8e2b38943fa9f05d4022e18a67b61fee)] make get_unique_path() return the same type as the input (str or Path)
- [[`57d019f`](https://gitlab.com/katalytic/katalytic-files/commit/57d019fe02df36a4b423502f96f5a9312bb8f9ed)] remove the 'error' option for make_dirs


## 0.10.0 (2023-06-01)
### feat
- [[`b2a6c34`](https://gitlab.com/katalytic/katalytic-files/commit/b2a6c345943e9fdb1b2972ca39f7541f5b0dda2d)] add exists and make_dirs parameters to the save_X functions
### fix
- [[`246cce3`](https://gitlab.com/katalytic/katalytic-files/commit/246cce364cf094a57d860c94def8ef7aee0d5bd0)] change {delete,move,copy}_{file,dir} defaults to be more convenient instead of safer
- [[`1cd06f4`](https://gitlab.com/katalytic/katalytic-files/commit/1cd06f420f3aa915b97c0bf752401a347bc4188a)] docstring not being shown for load() and save()
- [[`ff90a28`](https://gitlab.com/katalytic/katalytic-files/commit/ff90a28647d3a5c28b4f0129e19b723d16cb3e06)] make _get_all() and related functions return the same type as the input (str or Path)
- [[`449a83a`](https://gitlab.com/katalytic/katalytic-files/commit/449a83ae8e2b38943fa9f05d4022e18a67b61fee)] make get_unique_path() return the same type as the input (str or Path)
- [[`57d019f`](https://gitlab.com/katalytic/katalytic-files/commit/57d019fe02df36a4b423502f96f5a9312bb8f9ed)] remove the 'error' option for make_dirs


## 0.9.1 (2023-05-31)
### fix
- [[`7cdb066`](https://gitlab.com/katalytic/katalytic-files/commit/7cdb066ac2833fb9977ddffafb8f843d066ce1e8)] use the latest signature for sort_dict_by_keys()


## 0.9.0 (2023-05-22)
### feat
- [[`e339626`](https://gitlab.com/katalytic/katalytic-files/commit/e33962652287c979406ecc533da7a55e9cb58e50)] add ujson as optional dependency and try using it instead of the stdlib json for faster load/save
### refactor
- [[`00d80e2`](https://gitlab.com/katalytic/katalytic-files/commit/00d80e2b4b273e595a6f174750a0e69f29540387)] remove unused private function
- [[`69bd62b`](https://gitlab.com/katalytic/katalytic-files/commit/69bd62be521ca9cf2628eb36b79d327995b5509f)] replace private functions with the ones from katalytic.data
- [[`7ecef41`](https://gitlab.com/katalytic/katalytic-files/commit/7ecef418d0cd93f92da959c0c16d2ecdfd6c2218)] use is_none_of, is_any_of from katalytic-data


## 0.8.0 (2023-04-28)
### feat
- [[`43ef293`](https://gitlab.com/katalytic/katalytic-files/commit/43ef293431fafae20d13dbc2798cb78958fea4c4)] remove the encoding arg from load/save and the **kwargs from non-universal funcs


## 0.7.0 (2023-04-28)
### feat
- [[`1cb4276`](https://gitlab.com/katalytic/katalytic-files/commit/1cb4276ed44ff52b8aa33cdf65a358acee213712)] add load_csv() and save_csv()
- [[`d8c554c`](https://gitlab.com/katalytic/katalytic-files/commit/d8c554c8d993b1693b6e264a19c47a9352db9475)] add universal functions: load() and save()
- [[`7ee6498`](https://gitlab.com/katalytic/katalytic-files/commit/7ee6498a7eb7db0192d5dcfe94ce564d25e51082)] **load_csv:** convert empty strings to None
- [[`47bd254`](https://gitlab.com/katalytic/katalytic-files/commit/47bd254fe9fead96b08d75af0f2d878d51bc59c7)] **load/save:** lowercase the extension


## 0.6.1 (2023-04-16)
### Fix
* Test the new token ([`f2838d7`](https://github.com/katalytic/katalytic-files/commit/f2838d7ca49a27e8bbf718fab5d55b64868cf734))
* Test the new token ([`43d505a`](https://github.com/katalytic/katalytic-files/commit/43d505aab96beaa6807188d72aece63de7d9f812))


## 0.6.0 (2023-04-15)
### Feature
* Add load_text() and save_text() ([`2283da7`](https://github.com/katalytic/katalytic-files/commit/2283da70eddcc90f3ff90f14f9c611ffb310adf6))
* Add load_text() and save_text() ([`4eb85d6`](https://github.com/katalytic/katalytic-files/commit/4eb85d66245efad828f14b0ccd48858a473e9394))


## 0.5.0 (2023-04-15)
### Feature
* **load_json:** Remove sort_keys parameter. I will add a function for that later, probably in katalytic-data ([`8e188c0`](https://github.com/katalytic/katalytic-files/commit/8e188c08fc22497090f8ca07d8aaa47aa1856dd4))


## 0.4.0 (2023-04-15)
### Feature
* Add load_json() and save_json() ([`a4fed13`](https://github.com/katalytic/katalytic-files/commit/a4fed135abe77732c337b33ec65b0ffa69f8536d))
