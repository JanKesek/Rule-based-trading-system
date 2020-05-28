(defrule pricebuy
    (deltaprice big)
    (deltavolume big)
    (deltawbb big)
    =>
    (assert (price_decision buy)))
(defrule pricebuyhold
    (deltaprice big)
    (deltavolume big)
    (deltawbb low)
    =>
    (assert (price_decision buy_hold)))
;(defrule pricehold
;    (deltaprice big)
;    (deltavolume medium)
;    (deltawbb low)
;    =>
;    (assert (pricedecision hold)))
(defrule pricesell
    (deltaprice minusbig)
    (deltavolume big)
    (deltawbb big)
    =>
    (assert (price_decision sell)))
(defrule etabuy
    (deltaeta big)
    (deltavolume big)
    (deltawbb medium)
    =>
    (assert (eta_decision buy)))
(defrule etabuyhold
    (deltaeta big)
    (deltavolume big)
    (deltawbb low)
    =>
    (assert (eta_decision buy_hold)))
(defrule etasell
    (deltaeta minusbig)
    (deltavolume big)
    (deltawbb medium)
    =>
    (assert (eta_decision sell)))
(defrule etasellhold
    (deltaeta minusbig)
    (deltavolume big)
    (deltawbb low)
    =>
    (assert (eta_decision sell_hold)))
