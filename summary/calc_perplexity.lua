--
--  Copyright (c) 2015, Facebook, Inc.
--  All rights reserved.
--
--  This source code is licensed under the BSD-style license found in the
--  LICENSE file in the root directory of this source tree. An additional grant
--  of patent rights can be found in the PATENTS file in the same directory.
--
--  Author: Alexander M Rush <srush@seas.harvard.edu>
--          Sumit Chopra <spchopra@fb.com>
--          Jason Weston <jase@fb.com>

-- The top-level training script
require('torch')
require('nngraph')

local nnlm = require('summary.nnlm')
local data = require('summary.data')
local encoder  = require('summary.encoder')

nnlm:load('working_dir/models/model.20.th')

-- Load in the data.
local tdata = data.load_title('working_dir/processed/train/title/', true)
local article_data = data.load_article('working_dir/processed/train/article/')

local valid_data = data.load_title('working_dir/processed/valid.filter/title/', nil, tdata.dict)
local valid_article_data =
  data.load_article('working_dir/processed/valid.filter/article/', article_data.dict)

-- Make main LM
local valid = data.init(valid_data, valid_article_data)

nnlm:validation(valid)
