## 0.6.0 (2023-06-26)
### feat
- [[`7baa7e9`](https://gitlab.com/katalytic/katalytic-images/commit/7baa7e94f5786d23f6f87051e8c87c4cdfec1407)] when passing a PIL.Image to draw() or load_image(), return another PIL.Image
### refactor
- [[`eaa3cc6`](https://gitlab.com/katalytic/katalytic-images/commit/eaa3cc61705170539ec7076e63d86395ba57bf19)] make condition more explicit
- [[`0d16675`](https://gitlab.com/katalytic/katalytic-images/commit/0d16675d3075eae62f31560c1e326a18057009a6)] use errno codes instead of hardcoded numbers


## 0.5.0 (2023-06-02)
### feat
- [[`37afcb5`](https://gitlab.com/katalytic/katalytic-images/commit/37afcb5e74c8f6b081b8261136a873c291358cdd)] load_image(..., *, default=_UNDEFINED) and save_image(..., exists='replace', make_dirs=True, mode='RGB', ...)


## 0.4.1 (2023-05-31)
### fix
- [[`dc2fff6`](https://gitlab.com/katalytic/katalytic-images/commit/dc2fff66953ee47de40d78702ab6b55079800969)] ValueError -> TypeError
- [[`44c3801`](https://gitlab.com/katalytic/katalytic-images/commit/44c38013096021262cdb3c5e8da0ff50972468cb)] convert types to what opencv expects
- [[`c6fe7fa`](https://gitlab.com/katalytic/katalytic-images/commit/c6fe7fae2868c1340929704ba20cbcd303647aa1)] readme
- [[`ecaef54`](https://gitlab.com/katalytic/katalytic-images/commit/ecaef54965aaaec043b8fd170a5d82c15071a8df)] remove unnecessary function and convert circle radius to int


## 0.4.0 (2023-05-07)
### feat
- [[`dca7f3e`](https://gitlab.com/katalytic/katalytic-images/commit/dca7f3eb1ee463393fa8c872fcebe8f101b5f73c)] add create_{rectangle,circle,line,text,mask,polylines}


## 0.3.0 (2023-05-04)
### feat
- [[`d824d98`](https://gitlab.com/katalytic/katalytic-images/commit/d824d989ce58efd8ffe644e2527d02952a230a92)] **draw:** add more shape types
- [[`62be07d`](https://gitlab.com/katalytic/katalytic-images/commit/62be07dfbc5aca96d490732eaa421d6083c5d663)] **draw:** implement 'mask' and 'polylines' shape types


## 0.2.2 (2023-05-01)
### fix
- [[`acf64bf`](https://gitlab.com/katalytic/katalytic-images/commit/acf64bf7dd6a9cac64d83403bc4eb33a2eec9119)] **draw:** KeyError: "background"


## 0.2.1 (2023-05-01)
### fix
- [[`16b0fd1`](https://gitlab.com/katalytic/katalytic-images/commit/16b0fd1d66f06dff08afbdb22b4f319d7831db1e)] **draw:** change default font_scale from 1.75 to 1.25


## 0.2.0 (2023-05-01)
### feat
- [[`0088b92`](https://gitlab.com/katalytic/katalytic-images/commit/0088b92ebc8afcddde775357a57006c4ae492195)] add bhwc, hwc, hw
- [[`d33f595`](https://gitlab.com/katalytic/katalytic-images/commit/d33f595243f80d0ae5673622b5b4f6792786d63d)] add draw() and draw_inplace(); fix are_arrays_equal() when the shape is different
- [[`e7fb20b`](https://gitlab.com/katalytic/katalytic-images/commit/e7fb20b238ef1f63dc8ea79db2260271ca9f79a9)] add load_image and save_image to the universal functions


## 0.1.3 (2023-04-14)
### Fix
* Release ([`b05f06a`](https://github.com/katalytic/katalytic-images/commit/b05f06a0562caaaecb3ae78dd6167f6efd7bfdd9))


## 0.1.2 (2023-04-14)
### Fix
* Release ([`d8dcc26`](https://github.com/katalytic/katalytic-images/commit/d8dcc26a40c78db399546ed6b03d759de46c5368))
* Release ([`ca4c3a4`](https://github.com/katalytic/katalytic-images/commit/ca4c3a46dc9c845be9829176346a1a5e14c7eb09))
* Prep for travis ([`4533802`](https://github.com/katalytic/katalytic-images/commit/45338021cb605202ec63645780951545a28408e9))
* Prep for travis ([`a7ab07a`](https://github.com/katalytic/katalytic-images/commit/a7ab07abb5e2bbf5001f85039820ced1cbeec541))


