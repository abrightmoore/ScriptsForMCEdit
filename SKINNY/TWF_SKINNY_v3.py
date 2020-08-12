# @TheWorldFoundry
# This filter helps you edit Minecraft player skin file pngs from within MCEdit.
# You build a player in the world (or import one from a skin file) and then you can edit it like any other Minecraft build using a selection of blocks, and then export the model as a skin file's INNER or OUTER layer.
# The filter lets you layer the OUTER layer on an existing skin so you can develop a range of 'wearables' for your characters and adjust to suit over time.
# Have a play with it to see what it does!

import pygame
from pygame import *
from os import listdir
from os.path import isfile, join
import glob
import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *

inputs = (
		("SKINNY", "label"),
		("Skin file name", ("string","skin.png")),
		("Mode", ("Create 3D Character", "Save skin png")),
		("Outer?", False),
		("adrian@TheWorldFoundry.com", "label"),
		("http://theworldfoundry.com", "label"),
)

# Updated @abrightmoore v1.12 blocks and new matching attributes
materials = [

(0,"anvil_base.png", (145,0), 64, 64, 64, 64, 78, 78, 78),
(0,"anvil_top_damaged_0.png", (145,0), 64, 60, 60, 61, 75, 71, 71),
(0,"anvil_top_damaged_1.png", (145,1), 64, 60, 60, 61, 86, 82, 82),
(0,"anvil_top_damaged_2.png", (145,2), 64, 60, 60, 61, 91, 87, 87),
(0,"beacon.png", (138,0), 116, 221, 215, 184, 255, 255, 255),
(0,"bedrock.png", (7,0), 83, 83, 83, 83, 151, 151, 151),
(0,"beetroots_stage_0.png", (207,0), 1, 171, 16, 62, 5, 226, 23),
(0,"beetroots_stage_1.png", (207,1), 1, 187, 15, 67, 5, 226, 23),
(0,"beetroots_stage_2.png", (207,2), 0, 190, 16, 68, 5, 226, 23),
(0,"beetroots_stage_3.png", (207,3), 53, 132, 44, 76, 204, 224, 168),
(1,"bone_block_side.png", (216,0), 224, 220, 200, 215, 234, 231, 214),
(0,"bone_block_top.png", (216,0), 205, 201, 177, 194, 231, 228, 211),
(0,"bookshelf.png", (47,0), 107, 88, 57, 84, 188, 181, 181),
(0,"brewing_stand.png", (117,0), 124, 103, 81, 103, 228, 228, 228),
(0,"brewing_stand_base.png", (117,0), 106, 106, 106, 106, 159, 159, 159),
(1,"brick.png", (45,0), 146, 99, 86, 110, 184, 165, 159),
(0,"cactus_bottom.png", (81,0), 162, 186, 122, 156, 222, 223, 162),
(0,"cactus_side.png", (81,0), 14, 111, 27, 50, 20, 142, 36),
(0,"cactus_top.png", (81,0), 14, 113, 27, 51, 20, 148, 36),
(0,"cake_bottom.png", (92,0), 177, 89, 36, 100, 184, 93, 39),
(0,"cake_inner.png", (92,0), 132, 56, 26, 71, 234, 233, 235),
(0,"cake_side.png", (92,0), 188, 141, 113, 147, 234, 233, 235),
(0,"cake_top.png", (92,0), 228, 205, 206, 213, 234, 233, 235),
(0,"carrots_stage_0.png", (141,0), 1, 171, 16, 62, 5, 226, 23),
(0,"carrots_stage_1.png", (141,2), 1, 187, 15, 67, 5, 226, 23),
(0,"carrots_stage_2.png", (141,4), 0, 190, 16, 68, 5, 226, 23),
(0,"carrots_stage_3.png", (141,7), 21, 128, 2, 50, 226, 196, 24),
(0,"cauldron_bottom.png", (118,0), 44, 44, 44, 44, 45, 45, 45),
(0,"cauldron_inner.png", (118,0), 55, 55, 55, 55, 65, 65, 65),
(0,"cauldron_side.png", (118,0), 62, 62, 62, 62, 82, 82, 82),
(0,"cauldron_top.png", (118,0), 71, 71, 71, 71, 84, 84, 84),
(0,"chain_command_block_back.png", (211,0), 126, 150, 140, 139, 243, 210, 221),
(0,"chain_command_block_conditional.png", (211,0), 126, 155, 143, 141, 243, 210, 221),
(0,"chain_command_block_front.png", (211,0), 129, 159, 146, 144, 243, 207, 218),
(0,"chain_command_block_side.png", (211,0), 128, 154, 143, 141, 243, 210, 221),
(0,"chorus_flower.png", (200,0), 133, 103, 133, 123, 254, 254, 254),
(0,"chorus_flower_dead.png", (200,0), 98, 63, 96, 85, 207, 203, 186),
(0,"chorus_plant.png", (199,0), 96, 59, 96, 83, 186, 162, 186),
(1,"clay.png", (82,0), 158, 164, 176, 166, 175, 185, 214),
(1,"coal_block.png", (173,0), 18, 18, 18, 18, 43, 43, 43),
(0,"coal_ore.png", (16,0), 115, 115, 115, 115, 143, 143, 143),
(1,"coarse_dirt.png", (3,1), 119, 85, 59, 87, 185, 135, 135),
(0,"cobblestone.png", (4,0), 122, 122, 122, 122, 191, 191, 191),
(0,"cobblestone_mossy.png", (48,0), 103, 121, 103, 109, 199, 199, 199),
(0,"cocoa_stage_0.png", (127,0), 138, 140, 64, 114, 197, 203, 103),
(0,"cocoa_stage_1.png", (127,1), 137, 107, 51, 98, 213, 177, 117),
(0,"cocoa_stage_2.png", (127,2), 145, 80, 30, 85, 226, 177, 124),
(0,"command_block_back.png", (137,0), 164, 127, 107, 132, 232, 210, 221),
(0,"command_block_conditional.png", (137,0), 168, 129, 107, 134, 243, 210, 221),
(0,"command_block_front.png", (137,0), 172, 132, 108, 137, 243, 207, 218),
(0,"command_block_side.png", (137,0), 167, 129, 108, 134, 243, 210, 221),
(0,"comparator_off.png", (149,0), 156, 150, 149, 152, 232, 226, 217),
(0,"comparator_on.png", (150,0), 165, 149, 148, 154, 255, 205, 205),
(1,"concrete_black.png", (251,15), 8, 10, 15, 11, 10, 12, 17),
(1,"concrete_blue.png", (251,11), 44, 46, 143, 77, 46, 48, 144),
(1,"concrete_brown.png", (251,12), 96, 59, 31, 62, 97, 61, 33),
(1,"concrete_cyan.png", (251,9), 21, 119, 136, 92, 23, 120, 137),
(1,"concrete_gray.png", (251,7), 54, 57, 61, 57, 56, 59, 63),
(1,"concrete_green.png", (251,13), 73, 91, 36, 66, 74, 92, 38),
(1,"concrete_light_blue.png", (251,3), 35, 137, 198, 123, 38, 138, 200),
(1,"concrete_lime.png", (251,5), 94, 168, 24, 95, 96, 170, 27),
(1,"concrete_magenta.png", (251,2), 169, 48, 159, 125, 170, 50, 160),
(1,"concrete_orange.png", (251,1), 224, 97, 0, 107, 225, 99, 3),
(1,"concrete_pink.png", (251,6), 213, 101, 142, 151, 214, 103, 144),
(1,"concrete_powder_black.png", (252,15), 25, 26, 31, 27, 61, 61, 66),
(1,"concrete_powder_blue.png", (252,11), 70, 73, 166, 103, 89, 96, 197),
(1,"concrete_powder_brown.png", (252,12), 125, 84, 53, 87, 158, 116, 78),
(1,"concrete_powder_cyan.png", (252,4), 36, 147, 157, 113, 48, 208, 208),
(1,"concrete_powder_gray.png", (252,7), 76, 81, 84, 80, 101, 115, 119),
(1,"concrete_powder_green.png", (252,5), 97, 119, 44, 86, 121, 151, 57),
(1,"concrete_powder_light_blue.png", (252,3), 74, 180, 213, 155, 108, 221, 242),
(1,"concrete_powder_lime.png", (252,5), 125, 189, 41, 118, 181, 223, 122),
(1,"concrete_powder_magenta.png", (252,2), 192, 83, 184, 153, 223, 125, 216),
(1,"concrete_powder_orange.png", (252,1), 227, 131, 31, 129, 247, 180, 78),
(1,"concrete_powder_pink.png", (252,6), 228, 153, 181, 187, 247, 209, 224),
(1,"concrete_powder_purple.png", (252,10), 131, 55, 177, 121, 162, 73, 205),
(1,"concrete_powder_red.png", (252,14), 168, 54, 50, 90, 206, 91, 83),
(1,"concrete_powder_silver.png",(252,8), 154, 154, 148, 152, 191, 190, 182),
(1,"concrete_powder_white.png", (252,0), 225, 227, 227, 226, 253, 253, 253),
(1,"concrete_powder_yellow.png", (252,4), 232, 199, 54, 161, 249, 234, 181),
(1,"concrete_purple.png", (251,10), 100, 31, 156, 95, 101, 33, 157),
(1,"concrete_red.png", (251,14), 142, 32, 32, 68, 143, 35, 35),
(1,"concrete_silver.png", (251,8), 125, 125, 115, 121, 126, 126, 116),
(1,"concrete_white.png", (251,0), 207, 213, 214, 211, 209, 214, 215),
(1,"concrete_yellow.png", (251,4), 240, 175, 21, 145, 242, 177, 24),
(0,"crafting_table_front.png", (58,0), 115, 95, 63, 91, 255, 255, 255),
(0,"crafting_table_side.png", (58,0), 118, 95, 60, 91, 216, 216, 216),
(0,"crafting_table_top.png", (58,0), 107, 71, 42, 73, 186, 150, 96),
(0,"daylight_detector_inverted_top.png", (151,0), 106, 109, 112, 108, 195, 204, 217),
(0,"daylight_detector_side.png", (151,0), 66, 55, 35, 52, 86, 69, 43),
(0,"daylight_detector_top.png", (151,0), 130, 116, 94, 113, 228, 219, 206),
(0,"deadbush.png", (32,0), 123, 79, 25, 75, 148, 100, 40),
(0,"debug.png", (0,0), 177, 197, 203, 192, 255, 255, 255),
(0,"debug2.png", (0,0), 193, 187, 183, 187, 255, 255, 255),
(0,"destroy_stage_0.png", (0,0), 252, 252, 252, 252, 255, 255, 255),
(0,"destroy_stage_1.png", (0,0), 248, 248, 248, 248, 255, 255, 255),
(0,"destroy_stage_2.png", (0,0), 243, 243, 243, 243, 255, 255, 255),
(0,"destroy_stage_3.png", (0,0), 238, 238, 238, 238, 255, 255, 255),
(0,"destroy_stage_4.png", (0,0), 230, 230, 230, 230, 255, 255, 255),
(0,"destroy_stage_5.png", (0,0), 222, 222, 222, 222, 255, 255, 255),
(0,"destroy_stage_6.png", (0,0), 212, 212, 212, 212, 255, 255, 255),
(0,"destroy_stage_7.png", (0,0), 195, 195, 195, 195, 255, 255, 255),
(0,"destroy_stage_8.png", (0,0), 177, 177, 177, 177, 255, 255, 255),
(0,"destroy_stage_9.png", (0,0), 167, 167, 167, 167, 255, 255, 255),
(1,"diamond_block.png", (57,0), 97, 219, 213, 176, 170, 237, 234),
(0,"diamond_ore.png", (56,0), 129, 140, 143, 137, 255, 255, 255),
(1,"dirt.png", (3,0), 134, 96, 67, 98, 185, 135, 135),
(0,"dirt_podzol_side.png", (3,2), 122, 87, 57, 88, 185, 135, 135),
(0,"dirt_podzol_top.png", (3,2), 90, 63, 28, 60, 173, 106, 67),
(0,"dispenser_front_horizontal.png", (23,0), 117, 117, 117, 117, 200, 200, 200),
(0,"dispenser_front_vertical.png", (23,0), 87, 87, 87, 87, 157, 157, 157),
(0,"door_acacia_lower.png", (196,0), 155, 88, 54, 99, 195, 119, 111),
(0,"door_acacia_upper.png", (196,8), 160, 92, 58, 103, 195, 119, 114),
(0,"door_birch_lower.png", (194,0), 204, 194, 142, 180, 252, 248, 229),
(0,"door_birch_upper.png", (194,8), 218, 210, 175, 201, 253, 249, 230),
(0,"door_dark_oak_lower.png", (197,0), 65, 44, 23, 44, 224, 201, 111),
(0,"door_dark_oak_upper.png", (197,8), 69, 47, 25, 47, 255, 229, 111),
(0,"door_iron_lower.png", (71,0), 163, 163, 163, 163, 209, 209, 209),
(0,"door_iron_upper.png", (71,8), 186, 186, 186, 186, 207, 207, 207),
(0,"door_jungle_lower.png", (195,0), 150, 109, 78, 112, 206, 161, 130),
(0,"door_jungle_upper.png", (195,8), 156, 115, 84, 118, 206, 161, 130),
(0,"door_spruce_lower.png", (193,0), 97, 75, 49, 74, 162, 162, 162),
(0,"door_spruce_upper.png", (193,8), 96, 74, 49, 73, 138, 111, 111),
(0,"door_wood_lower.png", (64,0), 134, 101, 50, 95, 176, 151, 111),
(0,"door_wood_upper.png", (64,8), 134, 103, 51, 96, 176, 151, 111),
(0,"double_plant_fern_bottom.png", (175,3), 124, 124, 124, 124, 184, 184, 184),
(0,"double_plant_fern_top.png", (175,11), 126, 126, 126, 126, 186, 186, 186),
(0,"double_plant_grass_bottom.png", (175,12), 130, 138, 126, 131, 247, 247, 253),
(0,"double_plant_grass_top.png", (175,10), 135, 141, 133, 136, 247, 247, 253),
(0,"double_plant_paeonia_bottom.png", (175,5), 66, 81, 46, 64, 247, 224, 247),
(0,"double_plant_paeonia_top.png", (175,13), 192, 193, 197, 194, 255, 255, 255),
(0,"double_plant_rose_bottom.png", (175,4), 67, 66, 3, 45, 247, 156, 64),
(0,"double_plant_rose_top.png", (175,10), 86, 77, 5, 56, 247, 156, 64),
(0,"double_plant_sunflower_back.png", (175,0), 64, 120, 36, 73, 87, 164, 50),
(0,"double_plant_sunflower_bottom.png", (175,0), 95, 142, 86, 107, 247, 247, 253),
(0,"double_plant_sunflower_front.png", (175,0), 203, 195, 37, 145, 241, 228, 230),
(0,"double_plant_sunflower_top.png", (175,8), 95, 148, 84, 109, 247, 247, 253),
(0,"double_plant_syringa_bottom.png", (175,1), 126, 154, 117, 132, 247, 247, 253),
(0,"double_plant_syringa_top.png", (175,9), 131, 153, 120, 134, 247, 247, 253),
(0,"dragon_egg.png", (122,0), 12, 9, 15, 12, 45, 16, 51),
(0,"dropper_front_horizontal.png", (158,0), 118, 118, 118, 118, 200, 200, 200),
(0,"dropper_front_vertical.png", (158,0), 88, 88, 88, 88, 157, 157, 157),
(1,"emerald_block.png", (133,0), 81, 217, 117, 138, 146, 239, 172),
(0,"emerald_ore.png", (129,0), 109, 128, 116, 118, 217, 255, 235),
(0,"enchanting_table_bottom.png", (116,0), 18, 16, 27, 20, 70, 58, 96),
(0,"enchanting_table_side.png", (116,0), 41, 43, 46, 43, 255, 255, 255),
(0,"enchanting_table_top.png", (116,0), 103, 64, 59, 75, 255, 255, 255),
(0,"endframe_eye.png", (120,0), 40, 72, 67, 59, 204, 226, 215),
(0,"endframe_side.png", (120,0), 147, 160, 123, 143, 250, 250, 208),
(0,"endframe_top.png", (120,0), 89, 117, 96, 100, 249, 249, 197),
(1,"end_bricks.png", (206,0), 225, 230, 170, 208, 248, 249, 203),
(0,"end_rod.png", (198,0), 215, 190, 203, 202, 252, 252, 252),
(1,"end_stone.png", (121,0), 221, 223, 165, 202, 250, 250, 208),
(0,"farmland_dry.png", (60,0), 115, 75, 45, 78, 159, 111, 111),
(0,"farmland_wet.png", (60,7), 75, 40, 13, 42, 119, 64, 63),
(0,"fern.png", (31, 2), 120, 120, 120, 120, 181, 181, 181),
(0,"fire_layer_0.png", (51,0), 202, 127, 69, 132, 255, 255, 255),
(0,"fire_layer_1.png", (51,1), 197, 115, 52, 121, 255, 255, 255),
(0,"flower_allium.png", (38,2), 143, 146, 201, 163, 225, 241, 253),
(0,"flower_blue_orchid.png", (38,1), 45, 165, 174, 128, 247, 241, 253),
(0,"flower_dandelion.png", (37,0), 108, 162, 0, 90, 241, 249, 2),
(0,"flower_houstonia.png", (38,3), 134, 181, 186, 167, 242, 242, 253),
(0,"flower_oxeye_daisy.png", (38,8), 129, 172, 115, 138, 247, 247, 253),
(0,"flower_paeonia.png", (0,0), 130, 137, 146, 137, 240, 241, 253), # Unused
(0,"flower_pot.png", (140,0), 118, 65, 51, 78, 137, 76, 59),
(0,"flower_rose.png", (38,0), 99, 60, 5, 54, 247, 135, 54),
(0,"flower_tulip_orange.png", (38,5), 111, 150, 100, 120, 242, 242, 253),
(0,"flower_tulip_pink.png", (38,7), 110, 153, 109, 124, 243, 242, 253),
(0,"flower_tulip_red.png", (38,4), 118, 152, 112, 127, 242, 242, 253),
(0,"flower_tulip_white.png", (38,6), 110, 157, 111, 126, 243, 243, 253),
(1,"frosted_ice_0.png", (212,0), 125, 173, 255, 184, 255, 255, 255),
(0,"frosted_ice_1.png", (212,1), 132, 178, 255, 187, 255, 255, 255),
(0,"frosted_ice_2.png", (212,2), 137, 181, 255, 191, 255, 255, 255),
(0,"frosted_ice_3.png", (212,3), 147, 188, 255, 197, 255, 255, 255),
(0,"furnace_front_off.png", (61,0), 88, 88, 88, 88, 205, 205, 205),
(0,"furnace_front_on.png", (62,0), 133, 109, 90, 111, 252, 252, 243),
(0,"furnace_side.png", (61,0), 113, 113, 113, 113, 205, 205, 205),
(0,"furnace_top.png", (61,0), 96, 96, 96, 96, 163, 163, 163),
(0,"glass.png", (20,0), 218, 240, 244, 234, 254, 254, 254),
(0,"glass_black.png", (95,15), 25, 25, 25, 25, 25, 25, 25),
(0,"glass_blue.png", (95,11), 51, 76, 178, 101, 51, 76, 178),
(0,"glass_brown.png", (95,12), 102, 76, 51, 76, 102, 76, 51),
(0,"glass_cyan.png", (95,9), 76, 127, 153, 118, 76, 127, 153),
(0,"glass_gray.png", (95,7), 76, 76, 76, 76, 76, 76, 76),
(0,"glass_green.png", (95,13), 102, 127, 51, 93, 102, 127, 51),
(0,"glass_light_blue.png", (95,3), 102, 153, 216, 157, 102, 153, 216),
(0,"glass_lime.png", (95,5), 127, 204, 25, 118, 127, 204, 25),
(0,"glass_magenta.png", (95,2), 178, 76, 216, 156, 178, 76, 216),
(0,"glass_orange.png", (95,1), 216, 127, 51, 131, 216, 127, 51),
(0,"glass_pane_top.png", (102,0), 211, 239, 244, 231, 254, 254, 254),
(0,"glass_pane_top_black.png", (160,0), 24, 24, 24, 24, 25, 25, 25),
(0,"glass_pane_top_blue.png", (160,11), 48, 73, 171, 97, 50, 76, 177),
(0,"glass_pane_top_brown.png", (160,12), 97, 73, 48, 72, 101, 76, 50),
(0,"glass_pane_top_cyan.png", (160,9), 73, 122, 147, 114, 76, 127, 152),
(0,"glass_pane_top_gray.png", (160,7), 73, 73, 73, 73, 76, 76, 76),
(0,"glass_pane_top_green.png", (160,13), 97, 122, 48, 89, 101, 127, 50),
(0,"glass_pane_top_light_blue.png", (160,3), 97, 147, 208, 151, 101, 152, 215),
(0,"glass_pane_top_lime.png", (160,5), 122, 196, 24, 114, 127, 203, 25),
(0,"glass_pane_top_magenta.png", (160,2), 171, 73, 208, 151, 177, 76, 215),
(0,"glass_pane_top_orange.png", (160,1), 208, 122, 48, 126, 215, 127, 50),
(0,"glass_pane_top_pink.png", (160,6), 233, 122, 159, 171, 241, 127, 165),
(0,"glass_pane_top_purple.png", (160,10), 122, 61, 171, 118, 127, 63, 177),
(0,"glass_pane_top_red.png", (160,14), 147, 48, 48, 81, 152, 50, 50),
(0,"glass_pane_top_silver.png", (160,8), 147, 147, 147, 147, 152, 152, 152),
(0,"glass_pane_top_white.png", (160,0), 246, 246, 246, 246, 254, 254, 254),
(0,"glass_pane_top_yellow.png", (160,4), 221, 221, 48, 163, 228, 228, 50),
(0,"glass_pink.png", (95,6), 242, 127, 165, 178, 242, 127, 165),
(0,"glass_purple.png", (95,10), 127, 63, 178, 122, 127, 63, 178),
(0,"glass_red.png", (95,14), 153, 51, 51, 85, 153, 51, 51),
(0,"glass_silver.png", (95,8), 153, 153, 153, 153, 153, 153, 153),
(0,"glass_white.png", (95,0), 255, 255, 255, 255, 255, 255, 255),
(0,"glass_yellow.png", (95,4), 229, 229, 51, 169, 229, 229, 51),
(0,"glazed_terracotta_black.png", (250,0), 74, 32, 35, 47, 153, 65, 69),
(0,"glazed_terracotta_blue.png", (246,0), 47, 64, 139, 83, 69, 137, 211),
(0,"glazed_terracotta_brown.png", (247,0), 119, 106, 85, 103, 209, 154, 151),
(0,"glazed_terracotta_cyan.png", (244,0), 52, 118, 125, 98, 208, 214, 215),
(0,"glazed_terracotta_gray.png", (242,0), 83, 90, 93, 88, 157, 157, 157),
(0,"glazed_terracotta_green.png", (248,0), 117, 142, 67, 108, 208, 214, 215),
(0,"glazed_terracotta_light_blue.png", (238,0), 94, 164, 208, 155, 249, 255, 254),
(0,"glazed_terracotta_lime.png", (240,0), 162, 197, 55, 138, 255, 243, 196),
(0,"glazed_terracotta_magenta.png", (237,0), 208, 100, 191, 166, 244, 181, 218),
(0,"glazed_terracotta_orange.png", (236,0), 154, 147, 91, 131, 255, 255, 254),
(0,"glazed_terracotta_pink.png", (241,0), 235, 154, 181, 190, 244, 183, 203),
(0,"glazed_terracotta_purple.png", (245,0), 109, 48, 152, 103, 162, 84, 224),
(0,"glazed_terracotta_red.png", (249,0), 181, 59, 53, 97, 209, 145, 124),
(0,"glazed_terracotta_silver.png", (243,0), 144, 166, 167, 159, 213, 216, 217),
(0,"glazed_terracotta_white.png", (235,0), 188, 212, 202, 200, 254, 255, 254),
(0,"glazed_terracotta_yellow.png", (239,0), 234, 192, 88, 171, 255, 243, 196),
(0,"glowstone.png", (89,0), 143, 118, 69, 110, 255, 255, 255),
(1,"gold_block.png", (41,0), 249, 236, 78, 187, 255, 255, 120),
(0,"gold_ore.png", (14,0), 143, 139, 124, 136, 255, 255, 255),
(0,"grass_path_side.png", (208,0), 142, 105, 69, 105, 223, 195, 135),
(0,"grass_path_top.png", (208,0), 149, 124, 71, 115, 185, 162, 99),
(0,"grass_side.png", (2,0), 126, 107, 65, 99, 185, 203, 135),
(0,"grass_side_overlay.png", (2,0), 143, 143, 143, 143, 178, 178, 178),
(0,"grass_side_snowed.png", (2,1), 149, 120, 97, 122, 255, 255, 255),
(0,"grass_top.png", (2,0), 147, 147, 147, 147, 195, 195, 195),
(0,"gravel.png", (13,0), 126, 124, 122, 124, 183, 181, 182),
(1,"hardened_clay.png", (172,0), 150, 92, 66, 103, 160, 103, 77),
(1,"hardened_clay_stained_black.png", (159,15), 37, 22, 16, 25, 40, 25, 19),
(1,"hardened_clay_stained_blue.png", (159,11), 74, 59, 91, 74, 78, 64, 94),
(1,"hardened_clay_stained_brown.png", (159,12), 77, 51, 35, 54, 81, 55, 39),
(1,"hardened_clay_stained_cyan.png", (159,9), 86, 91, 91, 89, 93, 96, 96),
(1,"hardened_clay_stained_gray.png", (159,7), 57, 42, 35, 44, 61, 46, 38),
(1,"hardened_clay_stained_green.png", (159,13), 76, 83, 42, 66, 80, 87, 46),
(1,"hardened_clay_stained_light_blue.png", (159,3), 113, 108, 137, 119, 119, 112, 142),
(1,"hardened_clay_stained_lime.png", (159,5), 103, 117, 52, 91, 111, 123, 58),
(1,"hardened_clay_stained_magenta.png", (159,2), 149, 88, 108, 115, 156, 93, 114),
(1,"hardened_clay_stained_orange.png", (159,1), 161, 83, 37, 94, 169, 90, 44),
(1,"hardened_clay_stained_pink.png", (159,6), 161, 78, 78, 105, 169, 83, 84),
(1,"hardened_clay_stained_purple.png", (159,10), 118, 70, 86, 91, 126, 76, 92),
(1,"hardened_clay_stained_red.png", (159,14), 143, 61, 46, 83, 150, 66, 53),
(1,"hardened_clay_stained_silver.png", (159,8), 135, 106, 97, 112, 140, 110, 101),
(1,"hardened_clay_stained_white.png", (159,0), 209, 178, 161, 182, 214, 185, 166),
(1,"hardened_clay_stained_yellow.png", (159,4), 186, 133, 35, 117, 193, 139, 41),
(0,"hay_block_side.png", (170,0), 157, 116, 18, 97, 218, 183, 32),
(0,"hay_block_top.png", (170,0), 168, 139, 16, 107, 210, 175, 26),
(0,"hopper_inside.png", (154,0), 55, 55, 55, 55, 65, 65, 65),
(0,"hopper_outside.png", (154,0), 62, 62, 62, 62, 81, 81, 81),
(0,"hopper_top.png", (154,0), 67, 67, 67, 67, 84, 84, 84),
(1,"ice.png", (79,0), 125, 173, 255, 184, 255, 255, 255),
(1,"ice_packed.png", (174,0), 165, 194, 245, 201, 209, 224, 255),
(0,"iron_bars.png", (101,0), 109, 108, 106, 107, 174, 174, 175),
(1,"iron_block.png", (42,0), 219, 219, 219, 219, 243, 243, 243),
(0,"iron_ore.png", (15,0), 135, 130, 126, 130, 226, 192, 170),
(0,"iron_trapdoor.png", (167,0), 199, 199, 199, 199, 214, 214, 214),
(0,"itemframe_background.png", (0,0), 118, 68, 44, 76, 175, 92, 54), # Needs work
(0,"jukebox_side.png", (84,0), 100, 67, 50, 72, 155, 102, 75),
(0,"jukebox_top.png", (84,0), 107, 73, 55, 78, 155, 102, 75),
(0,"ladder.png", (65,0), 121, 95, 52, 89, 172, 136, 82),
(1,"lapis_block.png", (22,0), 38, 67, 137, 81, 69, 101, 170),
(0,"lapis_ore.png", (21,0), 102, 112, 134, 116, 143, 143, 204),
(0,"lava_flow.png", (10,0), 207, 91, 19, 106, 241, 203, 92),
(0,"lava_still.png", (11,0), 212, 90, 18, 106, 250, 235, 114),
(0,"leaves_acacia.png", (161,0), 135, 135, 135, 135, 187, 187, 187),
(0,"leaves_big_oak.png", (161,1), 135, 135, 135, 135, 187, 187, 187),
(0,"leaves_birch.png", (18,2), 135, 135, 135, 135, 187, 187, 187),
(0,"leaves_jungle.png", (18,3), 145, 142, 134, 140, 236, 220, 201),
(0,"leaves_oak.png", (18,0), 135, 135, 135, 135, 187, 187, 187),
(0,"leaves_spruce.png", (18,1), 116, 116, 116, 116, 154, 154, 154),
(0,"lever.png", (69,0), 106, 89, 64, 86, 149, 128, 128),
(1,"log_acacia.png", (162,12), 105, 99, 89, 97, 146, 138, 126),
(0,"log_acacia_top.png", (162,0), 154, 91, 64, 102, 196, 111, 101),
(1,"log_big_oak.png", (162,13), 52, 40, 23, 38, 82, 64, 38),
(0,"log_big_oak_top.png", (162,1), 78, 62, 41, 60, 109, 84, 53),
(1,"log_birch.png", (17,14), 206, 206, 201, 204, 255, 255, 255),
(0,"log_birch_top.png", (17,2), 184, 166, 121, 157, 255, 255, 255),
(1,"log_jungle.png", (17,15), 87, 67, 26, 60, 126, 105, 45),
(0,"log_jungle_top.png", (17,3), 153, 118, 73, 114, 201, 155, 111),
(1,"log_oak.png", (17,12), 102, 81, 49, 77, 159, 127, 80),
(0,"log_oak_top.png", (17,0), 154, 125, 77, 118, 201, 165, 111),
(1,"log_spruce.png", (17,13), 45, 28, 12, 28, 85, 58, 31),
(0,"log_spruce_top.png", (17,1), 104, 81, 48, 77, 148, 106, 57),
(0,"magma.png", (213,0), 135, 65, 25, 75, 248, 166, 68),
(0,"melon_side.png", (103,0), 141, 145, 36, 107, 190, 185, 55),
(0,"melon_stem_connected.png", (105,0), 139, 139, 139, 139, 215, 215, 215),
(0,"melon_stem_disconnected.png", (105,0), 153, 153, 153, 153, 215, 215, 215),
(0,"melon_top.png", (103,0), 151, 153, 36, 113, 190, 185, 45),
(0,"mob_spawner.png", (52,0), 26, 39, 49, 37, 40, 53, 64),
(0,"mushroom_block_inside.png", (99,0), 202, 171, 120, 164, 210, 177, 125),
(1,"mushroom_block_skin_brown.png", (99,0), 141, 106, 83, 110, 173, 134, 107),
(1,"mushroom_block_skin_red.png", (100,0), 182, 37, 36, 85, 222, 222, 222),
(0,"mushroom_block_skin_stem.png", (100,0), 207, 204, 194, 201, 218, 214, 204),
(0,"mushroom_brown.png", (39,0), 138, 105, 83, 109, 204, 153, 120),
(0,"mushroom_red.png", (40,0), 195, 53, 56, 101, 255, 255, 255),
(0,"mycelium_side.png", (110,0), 113, 88, 73, 91, 185, 135, 135),
(0,"mycelium_top.png", (110,0), 111, 99, 105, 105, 154, 135, 135),
(1,"netherrack.png", (87,0), 111, 54, 52, 72, 229, 170, 134),
(1,"nether_brick.png", (112,0), 44, 22, 26, 30, 74, 42, 48),
(1,"nether_wart_block.png", (214,0), 117, 6, 7, 43, 187, 48, 51),
(0,"nether_wart_stage_0.png", (115,0), 106, 14, 30, 50, 185, 48, 74),
(0,"nether_wart_stage_1.png", (115,1), 108, 15, 22, 48, 189, 49, 65),
(0,"nether_wart_stage_2.png", (115,3), 111, 18, 17, 48, 217, 70, 71),
(0,"noteblock.png", (25,0), 100, 67, 50, 72, 155, 102, 75),
(0,"observer_back.png", (218,0), 68, 66, 66, 67, 200, 200, 200),
(0,"observer_back_lit.png", (218,0), 72, 65, 65, 67, 255, 153, 152),
(0,"observer_front.png", (218,0), 105, 105, 105, 105, 197, 197, 197),
(0,"observer_side.png", (218,0), 62, 60, 60, 61, 114, 114, 114),
(0,"observer_top.png", (218,0), 97, 97, 97, 97, 163, 163, 163),
(1,"obsidian.png", (49,0), 20, 18, 29, 22, 70, 58, 96),
(0,"piston_bottom.png", (33,0), 96, 96, 96, 96, 163, 163, 163),
(0,"piston_inner.png", (33,0), 96, 96, 96, 96, 176, 176, 176),
(0,"piston_side.png", (33,0), 106, 102, 95, 101, 205, 205, 205),
(0,"piston_top_normal.png", (33,0), 153, 129, 89, 124, 239, 239, 239),
(0,"piston_top_sticky.png", (29,0), 141, 146, 99, 129, 239, 239, 239),
(1,"planks_acacia.png", (5,4), 169, 91, 51, 103, 186, 104, 59),
(1,"planks_big_oak.png", (5,5), 61, 39, 18, 39, 73, 47, 23),
(1,"planks_birch.png", (5,2), 195, 179, 123, 165, 215, 203, 141),
(1,"planks_jungle.png", (5,3), 154, 110, 77, 113, 184, 135, 100),
(1,"planks_oak.png", (5,0), 156, 127, 78, 120, 188, 152, 98),
(1,"planks_spruce.png", (5,1), 103, 77, 46, 76, 128, 94, 54),
(0,"portal.png", (90,0), 87, 10, 191, 96, 175, 92, 232),
(0,"potatoes_stage_0.png", (142,0), 1, 171, 16, 62, 5, 226, 23),
(0,"potatoes_stage_1.png", (142,2), 1, 187, 15, 67, 5, 226, 23),
(0,"potatoes_stage_2.png", (142,4), 0, 190, 16, 68, 5, 226, 23),
(0,"potatoes_stage_3.png", (142,7), 34, 170, 36, 80, 193, 224, 88),
(1,"prismarine_bricks.png", (168,1), 99, 160, 143, 134, 166, 207, 197),
(1,"prismarine_dark.png", (168,2), 59, 87, 75, 73, 94, 129, 115),
(1,"prismarine_rough.png", (168,0), 99, 152, 141, 131, 177, 214, 214),
(0,"pumpkin_face_off.png", (86,0), 142, 76, 12, 77, 227, 166, 75),
(0,"pumpkin_face_on.png", (91,0), 185, 133, 28, 115, 249, 255, 150),
(0,"pumpkin_side.png", (86,0), 197, 120, 23, 113, 227, 166, 75),
(0,"pumpkin_stem_connected.png", (104,0), 139, 139, 139, 139, 215, 215, 215),
(0,"pumpkin_stem_disconnected.png", (104,0), 153, 153, 153, 153, 215, 215, 215),
(0,"pumpkin_top.png", (86,0), 192, 118, 21, 110, 227, 170, 75),
(1,"purpur_block.png", (201,0), 166, 121, 166, 151, 199, 168, 199),
(0,"purpur_pillar.png", (202,0), 170, 126, 170, 155, 205, 173, 205),
(0,"purpur_pillar_top.png", (202,0), 170, 128, 170, 156, 205, 173, 205),
(0,"quartz_block_bottom.png", (155,0), 231, 228, 219, 226, 237, 235, 228),
(0,"quartz_block_chiseled.png", (155,1), 231, 228, 220, 226, 245, 244, 240),
(0,"quartz_block_chiseled_top.png", (155,1), 231, 228, 219, 226, 242, 240, 234),
(0,"quartz_block_lines.png", (155,2), 231, 227, 219, 225, 242, 240, 234),
(0,"quartz_block_lines_top.png", (155,2), 232, 229, 221, 227, 242, 240, 234),
(1,"quartz_block_side.png", (155,0), 236, 233, 226, 231, 242, 240, 234),
(0,"quartz_block_top.png", (155,0), 236, 233, 226, 231, 242, 240, 234),
(0,"quartz_ore.png", (153,0), 125, 84, 79, 96, 232, 226, 217),
(0,"rail_activator.png", (157,0), 115, 91, 68, 91, 245, 204, 164),
(0,"rail_activator_powered.png", (157,0), 148, 89, 67, 101, 243, 193, 164),
(0,"rail_detector.png", (28,0), 120, 101, 89, 103, 200, 189, 189),
(0,"rail_detector_powered.png", (28,0), 137, 92, 80, 103, 212, 168, 168),
(0,"rail_golden.png", (27,0), 132, 108, 72, 104, 245, 204, 164),
(0,"rail_golden_powered.png", (27,0), 154, 104, 70, 109, 243, 193, 164),
(0,"rail_normal.png", (66,0), 121, 108, 88, 105, 172, 164, 164),
(0,"rail_normal_turned.png", (66,0), 120, 107, 86, 104, 164, 164, 164),
(1,"redstone_block.png", (152,0), 171, 27, 9, 69, 228, 43, 19),
(0,"redstone_dust_dot.png", (55,0), 240, 240, 240, 240, 254, 254, 254),
(0,"redstone_dust_line0.png", (55,0), 240, 240, 240, 240, 254, 254, 254),
(0,"redstone_dust_line1.png", (55,0), 240, 240, 240, 240, 254, 254, 254),
(0,"redstone_lamp_off.png", (123,0), 70, 43, 26, 46, 176, 120, 83),
(0,"redstone_lamp_on.png", (124,0), 119, 89, 55, 87, 255, 255, 255),
(0,"redstone_ore.png", (75,0), 132, 107, 107, 115, 255, 143, 143),
(0,"redstone_torch_off.png", (75,0), 93, 62, 38, 64, 159, 127, 80),
(0,"redstone_torch_on.png", (76,0), 167, 75, 41, 94, 255, 255, 255),
(1,"red_nether_brick.png", (112,0), 68, 4, 6, 26, 138, 27, 31),
(0,"red_sand.png", (12,1), 169, 88, 33, 96, 200, 119, 60),
(0,"red_sandstone_bottom.png", (179,0), 162, 82, 27, 90, 180, 93, 34),
(0,"red_sandstone_carved.png", (179,1), 162, 82, 27, 90, 185, 95, 37),
(1,"red_sandstone_normal.png", (179,0), 165, 84, 29, 93, 186, 95, 37),
(1,"red_sandstone_smooth.png", (179,2), 168, 85, 30, 94, 185, 95, 37),
(0,"red_sandstone_top.png", (179,0), 166, 85, 29, 93, 182, 92, 34),
(0,"reeds.png", (83,0), 148, 192, 101, 147, 229, 239, 218),
(0,"repeater_off.png", (93,0), 151, 147, 147, 148, 205, 205, 205),
(0,"repeater_on.png", (94,0), 160, 147, 147, 151, 255, 205, 205),
(0,"repeating_command_block_back.png", (210,0), 121, 105, 162, 129, 243, 210, 221),
(0,"repeating_command_block_conditional.png", (210,0), 121, 105, 168, 131, 243, 210, 221),
(0,"repeating_command_block_front.png", (210,0), 123, 107, 171, 134, 243, 207, 218),
(0,"repeating_command_block_side.png", (210,0), 122, 106, 166, 131, 243, 210, 221),
(0,"sand.png", (12,0), 219, 211, 160, 196, 255, 255, 241),
(0,"sandstone_bottom.png", (24,0), 212, 205, 148, 188, 236, 230, 180),
(0,"sandstone_carved.png", (24,1), 215, 208, 154, 192, 242, 236, 196),
(1,"sandstone_normal.png", (24,0), 216, 209, 157, 194, 243, 236, 196),
(1,"sandstone_smooth.png", (24,2), 219, 211, 161, 197, 242, 236, 196),
(0,"sandstone_top.png", (24,0), 218, 210, 158, 195, 238, 229, 182),
(0,"sapling_acacia.png", (6,4), 100, 110, 21, 76, 142, 152, 33),
(0,"sapling_birch.png", (6,2), 118, 150, 84, 117, 207, 227, 186),
(0,"sapling_jungle.png", (6,3), 48, 86, 18, 50, 57, 128, 32),
(0,"sapling_oak.png", (6,0), 71, 102, 37, 70, 127, 173, 63),
(0,"sapling_roofed_oak.png", (6,5), 56, 89, 29, 58, 127, 173, 63),
(0,"sapling_spruce.png", (6,1), 51, 58, 33, 47, 80, 90, 57),
(1,"sea_lantern.png", (169,0), 172, 199, 190, 187, 229, 237, 231),
(0,"shulker_top_black.png", (234,0), 25, 25, 29, 26, 32, 32, 36),
(0,"shulker_top_blue.png", (230,0), 43, 45, 140, 76, 52, 54, 156),
(0,"shulker_top_brown.png", (231,0), 106, 66, 35, 69, 116, 72, 41),
(0,"shulker_top_cyan.png", (228,0), 20, 121, 135, 92, 22, 136, 146),
(0,"shulker_top_gray.png", (226,0), 55, 58, 62, 58, 62, 67, 71),
(0,"shulker_top_green.png", (232,0), 79, 100, 31, 70, 85, 110, 36),
(0,"shulker_top_light_blue.png", (222,0), 49, 163, 212, 141, 60, 182, 220),
(0,"shulker_top_lime.png", (224,0), 99, 172, 23, 98, 114, 189, 25),
(0,"shulker_top_magenta.png", (221,0), 173, 54, 163, 130, 188, 65, 177),
(0,"shulker_top_orange.png", (220,0), 234, 106, 8, 115, 245, 117, 18),
(0,"shulker_top_pink.png", (225,0), 230, 121, 157, 169, 244, 141, 171),
(0,"shulker_top_purple.png", (229,0), 139, 96, 139, 124, 151, 107, 151),
(0,"shulker_top_red.png", (233,0), 140, 31, 30, 66, 158, 38, 34),
(0,"shulker_top_silver.png", (227,0), 124, 124, 115, 121, 141, 141, 133),
(0,"shulker_top_white.png", (219,0), 215, 220, 221, 218, 232, 235, 236),
(0,"shulker_top_yellow.png", (223,0), 248, 188, 29, 155, 252, 200, 38),
(1,"slime.png", (165,0), 120, 200, 101, 140, 139, 218, 117),
(1,"snow.png", (80,0), 239, 251, 251, 247, 255, 255, 255),
(1,"soul_sand.png", (88,0), 84, 64, 51, 66, 154, 130, 115),
(0,"sponge.png", (19,0), 194, 195, 84, 158, 236, 238, 120),
(0,"sponge_wet.png", (19,1), 160, 158, 63, 127, 219, 218, 94),
(1,"stone.png", (1,0), 125, 125, 125, 125, 143, 143, 143),
(1,"stonebrick.png", (98,0), 122, 122, 122, 122, 164, 164, 164),
(0,"stonebrick_carved.png", (98,3), 118, 118, 118, 118, 160, 160, 160),
(0,"stonebrick_cracked.png", (98,2), 118, 118, 118, 118, 160, 160, 160),
(1,"stonebrick_mossy.png", (98,1), 114, 119, 106, 113, 164, 164, 164),
(1,"stone_andesite.png", (1,5), 130, 131, 131, 130, 205, 207, 194),
(1,"stone_andesite_smooth.png", (1,6), 133, 133, 134, 133, 190, 190, 186),
(1,"stone_diorite.png", (1,3), 179, 179, 182, 180, 244, 244, 245),
(1,"stone_diorite_smooth.png", (1,4), 183, 183, 185, 183, 242, 242, 243),
(1,"stone_granite.png", (1,1), 153, 113, 98, 121, 232, 217, 210),
(1,"stone_granite_smooth.png", (1,2), 159, 114, 98, 124, 214, 185, 173),
(0,"stone_slab_side.png", (44,0), 166, 166, 166, 166, 205, 205, 205),
(0,"stone_slab_top.png", (44,0), 159, 159, 159, 159, 176, 176, 176),
(0,"structure_block.png", (255,0), 88, 74, 90, 84, 215, 194, 215),
(0,"structure_block_corner.png", (255,0), 68, 57, 69, 65, 215, 194, 215),
(0,"structure_block_data.png", (255,0), 79, 65, 80, 75, 215, 194, 215),
(0,"structure_block_load.png", (255,0), 69, 57, 70, 65, 215, 194, 215),
(0,"structure_block_save.png", (255,0), 86, 71, 87, 81, 215, 194, 215),
(0,"tallgrass.png", (31,0), 135, 135, 135, 135, 183, 183, 183),
(0,"tnt_bottom.png", (46,0), 170, 77, 51, 99, 219, 142, 142),
(0,"tnt_side.png", (46,0), 185, 101, 78, 121, 219, 219, 219),
(0,"tnt_top.png", (46,0), 154, 77, 56, 95, 219, 142, 142),
(0,"torch_on.png", (50,0), 130, 106, 58, 98, 255, 255, 255),
(0,"trapdoor.png", (96,0), 144, 116, 75, 111, 255, 255, 255),
(0,"trip_wire.png", (132,0), 129, 129, 129, 129, 206, 206, 206),
(0,"trip_wire_source.png", (132,0), 138, 129, 113, 127, 188, 152, 148),
(0,"vine.png", (106,0), 111, 111, 111, 111, 170, 170, 170),
(0,"waterlily.png",(111,0), 118, 118, 118, 118, 150, 150, 150),
(0,"water_flow.png", (8,0), 49, 71, 244, 121, 73, 118, 245),
(0,"water_overlay.png", (9,0), 47, 67, 244, 119, 47, 67, 244),
(0,"water_still.png", (9,0), 46, 67, 244, 118, 73, 118, 245),
(0,"web.png", (30,0), 220, 220, 220, 220, 255, 255, 255),
(0,"wheat_stage_0.png", (59,0), 0, 179, 18, 65, 5, 226, 23),
(0,"wheat_stage_1.png", (59,1), 18, 172, 15, 68, 61, 229, 24),
(0,"wheat_stage_2.png", (59,2), 28, 137, 11, 59, 107, 218, 21),
(0,"wheat_stage_3.png", (59,3), 37, 139, 8, 61, 126, 206, 18),
(0,"wheat_stage_4.png", (59,4), 46, 128, 7, 60, 130, 224, 23),
(0,"wheat_stage_5.png", (59,5), 66, 123, 7, 65, 146, 205, 18),
(0,"wheat_stage_6.png", (59,6), 81, 120, 7, 69, 159, 210, 18),
(0,"wheat_stage_7.png", (59,7), 86, 102, 7, 65, 165, 191, 21),
(1,"wool_colored_yellow.png", (35,4), 248, 197, 39, 161, 254, 217, 63),
(1,"wool_colored_black.png", (35,15),20, 21, 25, 22, 37, 37, 41),
(1,"wool_colored_blue.png", (35,11),53, 57, 157, 88, 62, 77, 178),
(1,"wool_colored_brown.png", (35,12),114, 71, 40, 75, 131, 84, 50),
(1,"wool_colored_cyan.png", (35,9),21, 137, 145, 101, 22, 155, 156),
(1,"wool_colored_gray.png", (35,7),62, 68, 71, 67, 71, 79, 82),
(1,"wool_colored_green.png", (35,13),84, 109, 27, 73, 101, 134, 36),
(1,"wool_colored_light_blue.png", (35,3),58, 175, 217, 149, 78, 197, 231),
(1,"wool_colored_lime.png", (35,5),112, 185, 25, 107, 134, 204, 38),
(1,"wool_colored_magenta.png", (35,2),189, 68, 179, 145, 214, 96, 209),
(1,"wool_colored_orange.png", (35,1),240, 118, 19, 125, 249, 147, 43),
(1,"wool_colored_pink.png", (35,6), 237, 141, 172, 183, 244, 178, 201),
(1,"wool_colored_purple.png", (35,10), 121, 42, 172, 111, 151, 67, 205),
(1,"wool_colored_red.png", (35,14), 160, 39, 34, 77, 184, 52, 44),
(1,"wool_colored_silver.png", (35,8), 142, 142, 134, 139, 157, 157, 151),
(1,"wool_colored_white.png", (35,0), 233, 236, 236, 235, 254, 254, 254),
]


GEOMETRY = [
					["HEAD_TOP",8,0,"H",4,31,0,8,8,-1,-1],
					["HEAD_BOTTOM",16,0,"H",4,24,0,8,8,-1,-1],
					["HEAD_RIGHT",16,8,"VZ",4,24,0,8,8,1,-1],
					["HEAD_FRONT",8,8,"VX",4,24,0,8,8,-1,-1],
					["HEAD_LEFT",0,8,"VZ",11,24,0,8,8,-1,-1],
					["HEAD_BACK",24,8,"VX",4,24,7,8,8,1,-1],

					["HELMET_OUTER_TOP",40,0,"H",4,31,0,8,8,-1,-1],
					["HELMET_OUTER_BOTTOM",48,0,"H",4,24,0,8,8,-1,-1],					
					["HELMET_OUTER_RIGHT",48,8,"VZ",4,24,0,8,8,1,-1],
					["HELMET_OUTER_FRONT",40,8,"VX",4,24,0,8,8,-1,-1],
					["HELMET_OUTER_LEFT",32,8,"VZ",11,24,0,8,8,-1,-1],
					["HELMET_OUTER_BACK",56,8,"VX",4,24,7,8,8,1,-1],

					["LEG_RIGHT_TOP",20,48,"H",4,11,2,4,4,-1,-1],
					["LEG_RIGHT_BOTTOM",24,48,"H",4,0,2,4,4,-1,-1],
					["LEG_RIGHT_RIGHT",24,52,"VZ",4,0,2,4,12,1,-1],
					["LEG_RIGHT_FRONT",20,52,"VX",4,0,2,4,12,-1,-1],
					["LEG_RIGHT_LEFT",16,52,"VZ",9,0,2,4,12,-1,-1],
					["LEG_RIGHT_BACK",28,52,"VX",4,0,5,4,12,1,-1],
					
					["LEG_RIGHT_OUTER_TOP",4,48,"H",4,11,2,4,4,-1,-1],
					["LEG_RIGHT_OUTER_BOTTOM",8,48,"H",4,0,2,4,4,-1,-1],
					["LEG_RIGHT_OUTER_RIGHT",8,52,"VZ",4,0,2,4,12,1,-1],
					["LEG_RIGHT_OUTER_FRONT",4,52,"VX",4,0,2,4,12,-1,-1],
					["LEG_RIGHT_OUTER_LEFT",0,52,"VZ",9,0,2,4,12,-1,-1],
					["LEG_RIGHT_OUTER_BACK",12,52,"VX",4,0,5,4,12,1,-1],

					["LEG_LEFT_TOP",4,16,"H",8,11,2,4,4,-1,-1],
					["LEG_LEFT_BOTTOM",8,16,"H",8,0,2,4,4,-1,-1],
					["LEG_LEFT_RIGHT",8,20,"VZ",8,0,2,4,12,1,-1],
					["LEG_LEFT_FRONT",4,20,"VX",8,0,2,4,12,-1,-1],
					["LEG_LEFT_LEFT",0,20,"VZ",11,0,2,4,12,-1,-1],
					["LEG_LEFT_BACK",12,20,"VX",8,0,5,4,12,1,-1],
					
					["LEG_LEFT_OUTER_TOP",4,32,"H",8,11,2,4,4,-1,-1],
					["LEG_LEFT_OUTER_BOTTOM",8,32,"H",8,0,2,4,4,-1,-1],
					["LEG_LEFT_OUTER_RIGHT",8,36,"VZ",8,0,2,4,12,1,-1],
					["LEG_LEFT_OUTER_FRONT",4,36,"VX",8,0,2,4,12,-1,-1],
					["LEG_LEFT_OUTER_LEFT",0,36,"VZ",11,0,2,4,12,-1,-1],
					["LEG_LEFT_OUTER_BACK",12,36,"VX",8,0,5,4,12,1,-1],
					
					["TORSO_TOP",20,16,"H",4,23,2,8,4,-1,-1],
					["TORSO_BOTTOM",28,16,"H",4,12,2,8,4,-1,-1],
					["TORSO_RIGHT",28,20,"VZ",4,12,2,4,12,1,-1],
					["TORSO_FRONT",20,20,"VX",4,12,2,8,12,-1,-1],
					["TORSO_LEFT",16,20,"VZ",11,12,2,4,12,-1,-1],
					["TORSO_BACK",32,20,"VX",4,12,5,8,12,1,-1],

					["TORSO_OUTER_TOP",20,32,"H",4,23,2,8,4,-1,-1],
					["TORSO_OUTER_BOTTOM",28,32,"H",4,12,2,8,4,-1,-1],
					["TORSO_OUTER_RIGHT",28,36,"VZ",4,12,2,4,12,1,-1],
					["TORSO_OUTER_FRONT",20,36,"VX",4,12,2,8,12,-1,-1],
					["TORSO_OUTER_LEFT",16,36,"VZ",11,12,2,4,12,-1,-1],
					["TORSO_OUTER_BACK",32,36,"VX",4,12,5,8,12,1,-1],
					
					["ARM_RIGHT_TOP",36,48,"H",0,23,2,4,4,-1,-1],
					["ARM_RIGHT_BOTTOM",40,48,"H",0,12,2,4,4,-1,-1],
					["ARM_RIGHT_RIGHT",40,52,"VZ",0,12,2,4,12,1,-1],
					["ARM_RIGHT_FRONT",36,52,"VX",0,12,2,4,12,-1,-1],
					["ARM_RIGHT_LEFT",32,52,"VZ",3,12,2,4,12,-1,-1],
					["ARM_RIGHT_BACK",44,52,"VX",0,12,5,4,12,1,-1],

					["ARM_RIGHT_OUTER_TOP",52,48,"H",0,23,2,4,4,-1,-1],
					["ARM_RIGHT_OUTER_BOTTOM",56,48,"H",0,12,2,4,4,-1,-1],
					["ARM_RIGHT_OUTER_RIGHT",56,52,"VZ",0,12,2,4,12,1,-1],
					["ARM_RIGHT_OUTER_FRONT",52,52,"VX",0,12,2,4,12,-1,-1],
					["ARM_RIGHT_OUTER_LEFT",48,52,"VZ",3,12,2,4,12,-1,-1],
					["ARM_RIGHT_OUTER_BACK",60,52,"VX",0,12,5,4,12,1,-1],
					
					["ARM_LEFT_TOP",44,16,"H",12,23,2,4,4,-1,-1],
					["ARM_LEFT_BOTTOM",48,16,"H",12,12,2,4,4,-1,-1],
					["ARM_LEFT_RIGHT",48,20,"VZ",12,12,2,4,12,1,-1],
					["ARM_LEFT_FRONT",44,20,"VX",12,12,2,4,12,-1,-1],
					["ARM_LEFT_LEFT",40,20,"VZ",15,12,2,4,12,-1,-1],
					["ARM_LEFT_BACK",52,20,"VX",12,12,5,4,12,1,-1],
					
					["ARM_LEFT_OUTER_TOP",44,32,"H",12,23,2,4,4,-1,-1],
					["ARM_LEFT_OUTER_BOTTOM",48,32,"H",12,12,2,4,4,-1,-1],
					["ARM_LEFT_OUTER_RIGHT",48,36,"VZ",12,12,2,4,12,1,-1],
					["ARM_LEFT_OUTER_FRONT",44,36,"VX",12,12,2,4,12,-1,-1],
					["ARM_LEFT_OUTER_LEFT",40,36,"VZ",15,12,2,4,12,-1,-1],
					["ARM_LEFT_OUTER_BACK",52,36,"VX",12,12,5,4,12,1,-1],
			]

			
def perform(level,box,options):
	if options["Mode"] == "Save skin png":
		skinny3DtoImage(level,box,options)
	elif options["Mode"] == "Create 3D Character":
		skinnyImageto3D(level,box,options)
	
	level.markDirtyBox(box)	

def getColourProximity((r,g,b),(r1,g1,b1)):
	# This gives a colour in the RGB colour cube. Find out what angles these are
	disth2 = r**2+g**2
	theta = atan2(r,g)
	phi = atan2(b,sqrt(disth2))

	disth2_1 = r1**2+g1**2
	theta_1 = atan2(r1,g1)
	phi_1 = atan2(b1,sqrt(disth2_1))

	deltaTheta = theta-theta_1
	deltaPhi = phi-phi_1

	return (deltaTheta,deltaPhi)

library = {}
	
def closestMaterial((r, g, b, a)):
	key = str(r)+" "+str(g)+" "+str(b)
	if key in library:
		result = library[key]
		return result

	matched = ((35,15),pi,512,512)
	for m in materials:
		(isBuildBlock, textureFileName, (matID,matData), mr, mg, mb, mavg, mpr, mpg, mpb) = m # unpack
		if isBuildBlock == 1: # This block is a candidate.
			(theta, phi) = getColourProximity((r,g,b),(mr,mg,mb))
			dAngles = abs(theta)+abs(phi) # Summarise the angle gap
			dRed = r-mr
			dGreen = g-mg
			dBlue = b-mb
			dGap = sqrt(dRed**2+dGreen**2+dBlue**2)
			vecLength = sqrt(mr**2+mg**2+mb**2)
			colLength = sqrt(r**2+g**2+b**2)
			
			(matchMat,matchAngle,matchGap,matchLength) = matched
			
			if matID == 35 and matData == 1:
				print "Orange Wool"
				print (r,g,b),(theta,phi),(dAngles,dGap)

			
			if dAngles < matchAngle:
				if abs(colLength-vecLength) < 2*abs(colLength-matchLength):
					matched = ((matID, matData), dAngles, dGap, vecLength)

				print "Better match "+str((r,g,b))+" "+str((mr,mg,mb))+" "+str(matched)
			elif dGap < matchGap/3: # If colour isn't a good match, but the point is much, much closer
					matched = ((matID, matData), dAngles, dGap, vecLength)
					print "Length match "+str((r,g,b))+" "+str((mr,mg,mb))+" "+str(matched)
					
	(matchMat,matchAngle,matchGap,matchLength) = matched
	
	library[key] = matchMat
	return matchMat
	
def skinnyImageto3D(level,box,options):
	'''
		Scan the png file and generate a 3D model from the player skin
	'''	
	filename = options["Skin file name"]
	print "Reading skin file from",filename
	img = pygame.image.load(filename)
	
	for (key,pngx,pngy,dir,x,y,z,dim1,dim2,delta1,delta2) in GEOMETRY:
		if (options["Outer?"] == False and "OUTER" not in key) or (options["Outer?"] == True and "OUTER" in key):
			print "Processing",key
			for i in xrange(0,dim1):
				for j in xrange(0,dim2):
					px,py,pz = box.minx+x,box.miny+y,box.minz+z
					if dir == "H":
						px += i
						pz += j
					elif dir == "VX":
						px += i
						py += j
					elif dir == "VZ":
						pz += i
						py += j

					offset1 = 0
					offset2 = 0
					if delta1 < 0:
						offset1 = -1
					if delta2 < 0:
						offset2 = -1
						
					ppx = i
					if delta1 < 0:
						ppx = dim1-i-1
					ppy = j
					if delta2 <0:
						ppy = dim2-j-1

					(R,G,B,A) = img.get_at((pngx+ppx, pngy+ppy))
					
					
					if A > 0:
						(bid,bdata) = closestMaterial((R,G,B,A))
						level.setBlockAt(px,py,pz,bid)
						level.setBlockDataAt(px,py,pz,bdata)			
	
	
def skinny3DtoImage(level,box,options):
	'''
		Scan the selection and generate a player skin from the blocks at certain positions
	'''

	# For each part of the selection, check what block it is, and then plot the corresponding pixel colours from the materials[] set above

	filename = options["Skin file name"]
	print "Reading skin file from",filename
	try:
		img = pygame.image.load(filename)
	except:
		print "Unable to load skin file from",filename
		print "Creating a new skin image"
		img = pygame.Surface((64,64),SRCALPHA)
	
	# 
	for (key,pngx,pngy,dir,x,y,z,dim1,dim2,delta1,delta2) in GEOMETRY:
		if (options["Outer?"] == False and "OUTER" not in key) or (options["Outer?"] == True and "OUTER" in key):
			print "Processing",key
			for i in xrange(0,dim1):
				for j in xrange(0,dim2):
					px,py,pz = box.minx+x,box.miny+y,box.minz+z
					if dir == "H":
						px += i
						pz += j
					elif dir == "VX":
						px += i
						py += j
					elif dir == "VZ":
						pz += i
						py += j
					block = level.blockAt(px,py,pz)
					data = level.blockDataAt(px,py,pz)
					if (block,data) != (0,0): # Not AIR
						for (bflag,bname, (bid,bdata), bR, bG, bB, bAvg, bRP, bGP, bBP) in materials:
							if (bid,bdata) == (block,data):
								(R,G,B) = (bR,bG,bB)
								offset1 = 0
								offset2 = 0
								if delta1 < 0:
									offset1 = -1
								if delta2 < 0:
									offset2 = -1
									
								ppx = i
								if delta1 < 0:
									ppx = dim1-i-1
								ppy = j
								if delta2 <0:
									ppy = dim2-j-1
								img.set_at((pngx+ppx, pngy+ppy), (R,G,B,255))

	filename = options["Skin file name"]
	print "Writing skin file to",filename
	pygame.image.save(img,filename)								

	

