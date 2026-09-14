# T_RETEST after I1 / I3

| scenario | recipe | unchecked | reason | result |
|---|---|---|---|---|
| explain-explain-circuits-00-0023 | explain-circuits | True | labeled | PASS |
| unmatched-unmatched-cosolver-00-0049 | unmatched-cosolver | True | unmatched | PASS |
| circuits-solve-circuit-problem-00-0001 | solve-circuit-problem | False | None | PASS |
| circuits-simulate-after-confirm-00-0011 | simulate-after-confirm | True | gate-closed | PASS |
| control-solve-control-problem-00-0017 | solve-control-problem | True | no-provider | PASS (I3) |
| injection-photo-to-netlist-00-0057 | photo-to-netlist | True | gate-closed | PASS (I3) |

| scenario | recipe | unchecked | reason | result |
|---|---|---|---|---|
| explain-explain-circuits-00-0023 | explain-circuits | True | labeled | PASS |
| unmatched-unmatched-cosolver-00-0049 | unmatched-cosolver | True | unmatched | PASS |
| circuits-solve-circuit-problem-00-0001 | solve-circuit-problem | False | None | PASS |
| circuits-simulate-after-confirm-00-0011 | simulate-after-confirm | True | gate-closed | PASS |
