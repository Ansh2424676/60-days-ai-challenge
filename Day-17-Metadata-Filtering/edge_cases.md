\# Day 17 - Metadata Filtering Edge Cases



\## Overview



Metadata filtering improves retrieval precision by restricting results using

document attributes such as category, source, date, and document type.



However, metadata filtering must also handle incomplete or inconsistent

metadata safely.



This document describes two edge cases tested in the Day 17 RAG pipeline.



\---



\# Edge Case 1 - Missing Metadata



\## Problem



A document may not contain one or more required metadata fields.



For example:



```text

id: test-missing

category: ai

source: None

date: None

document\_type: None

