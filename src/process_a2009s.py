#!/usr/bin/env python3
#
# Need in path: /usr/local/freesurfer/python/bin

import argparse
import os
import pandas
import string

print(f'Running {__file__}')

pandas.set_option('display.max_rows', None)

parser = argparse.ArgumentParser()
parser.add_argument('--csv_dir', required=True)
parser.add_argument('--out_dir', required=True)
args = parser.parse_args()

# Function to sanitize varnames. Alphanumeric or underscore only
def sanitize(input_string):
    validchars = string.ascii_letters + string.digits + '_'
    output_string = ''
    for i in input_string:
        if i in validchars:
            output_string += i.lower()
        else:
            output_string += '_'
    return output_string

# Load freesurfer volumes data
area_lh = pandas.read_csv(os.path.join(args.csv_dir,'lh-aparc.a2009s-area.csv'))
area_rh = pandas.read_csv(os.path.join(args.csv_dir,'rh-aparc.a2009s-area.csv'))
vol_lh = pandas.read_csv(os.path.join(args.csv_dir,'lh-aparc.a2009s-volume.csv'))
vol_rh = pandas.read_csv(os.path.join(args.csv_dir,'rh-aparc.a2009s-volume.csv'))
thk_lh = pandas.read_csv(os.path.join(args.csv_dir,'lh-aparc.a2009s-thickness.csv'))
thk_rh = pandas.read_csv(os.path.join(args.csv_dir,'rh-aparc.a2009s-thickness.csv'))

# Drop first columns (subject label)
area_lh = area_lh.drop(area_lh.columns[0], axis=1)
area_rh = area_rh.drop(area_rh.columns[0], axis=1)
vol_lh = vol_lh.drop(vol_lh.columns[0], axis=1)
vol_rh = vol_rh.drop(vol_rh.columns[0], axis=1)
thk_lh = thk_lh.drop(thk_lh.columns[0], axis=1)
thk_rh = thk_rh.drop(thk_rh.columns[0], axis=1)

# Concatenate
aparc = pandas.concat(
    [
        area_lh, 
        area_rh, 
        vol_lh, 
        vol_rh,
        thk_lh, 
        thk_rh,
    ],
    axis=1)

# Sanitize varnames
aparc.columns = [sanitize(x) for x in aparc.columns]

# Remove duplicate columns (e.g. etiv)
aparc = aparc.loc[:,~aparc.columns.duplicated()].copy()

# Show cols
#for x in aparc.columns:
#    print(f"    '{x}',")

# Use known list of desired outputs. Fill with 0 any missing (and drop any
# that are unexpected)
rois = [
    'lh_g_and_s_frontomargin_area',
    'lh_g_and_s_occipital_inf_area',
    'lh_g_and_s_paracentral_area',
    'lh_g_and_s_subcentral_area',
    'lh_g_and_s_transv_frontopol_area',
    'lh_g_and_s_cingul_ant_area',
    'lh_g_and_s_cingul_mid_ant_area',
    'lh_g_and_s_cingul_mid_post_area',
    'lh_g_cingul_post_dorsal_area',
    'lh_g_cingul_post_ventral_area',
    'lh_g_cuneus_area',
    'lh_g_front_inf_opercular_area',
    'lh_g_front_inf_orbital_area',
    'lh_g_front_inf_triangul_area',
    'lh_g_front_middle_area',
    'lh_g_front_sup_area',
    'lh_g_ins_lg_and_s_cent_ins_area',
    'lh_g_insular_short_area',
    'lh_g_occipital_middle_area',
    'lh_g_occipital_sup_area',
    'lh_g_oc_temp_lat_fusifor_area',
    'lh_g_oc_temp_med_lingual_area',
    'lh_g_oc_temp_med_parahip_area',
    'lh_g_orbital_area',
    'lh_g_pariet_inf_angular_area',
    'lh_g_pariet_inf_supramar_area',
    'lh_g_parietal_sup_area',
    'lh_g_postcentral_area',
    'lh_g_precentral_area',
    'lh_g_precuneus_area',
    'lh_g_rectus_area',
    'lh_g_subcallosal_area',
    'lh_g_temp_sup_g_t_transv_area',
    'lh_g_temp_sup_lateral_area',
    'lh_g_temp_sup_plan_polar_area',
    'lh_g_temp_sup_plan_tempo_area',
    'lh_g_temporal_inf_area',
    'lh_g_temporal_middle_area',
    'lh_lat_fis_ant_horizont_area',
    'lh_lat_fis_ant_vertical_area',
    'lh_lat_fis_post_area',
    'lh_pole_occipital_area',
    'lh_pole_temporal_area',
    'lh_s_calcarine_area',
    'lh_s_central_area',
    'lh_s_cingul_marginalis_area',
    'lh_s_circular_insula_ant_area',
    'lh_s_circular_insula_inf_area',
    'lh_s_circular_insula_sup_area',
    'lh_s_collat_transv_ant_area',
    'lh_s_collat_transv_post_area',
    'lh_s_front_inf_area',
    'lh_s_front_middle_area',
    'lh_s_front_sup_area',
    'lh_s_interm_prim_jensen_area',
    'lh_s_intrapariet_and_p_trans_area',
    'lh_s_oc_middle_and_lunatus_area',
    'lh_s_oc_sup_and_transversal_area',
    'lh_s_occipital_ant_area',
    'lh_s_oc_temp_lat_area',
    'lh_s_oc_temp_med_and_lingual_area',
    'lh_s_orbital_lateral_area',
    'lh_s_orbital_med_olfact_area',
    'lh_s_orbital_h_shaped_area',
    'lh_s_parieto_occipital_area',
    'lh_s_pericallosal_area',
    'lh_s_postcentral_area',
    'lh_s_precentral_inf_part_area',
    'lh_s_precentral_sup_part_area',
    'lh_s_suborbital_area',
    'lh_s_subparietal_area',
    'lh_s_temporal_inf_area',
    'lh_s_temporal_sup_area',
    'lh_s_temporal_transverse_area',
    'lh_whitesurfarea_area',
    'rh_g_and_s_frontomargin_area',
    'rh_g_and_s_occipital_inf_area',
    'rh_g_and_s_paracentral_area',
    'rh_g_and_s_subcentral_area',
    'rh_g_and_s_transv_frontopol_area',
    'rh_g_and_s_cingul_ant_area',
    'rh_g_and_s_cingul_mid_ant_area',
    'rh_g_and_s_cingul_mid_post_area',
    'rh_g_cingul_post_dorsal_area',
    'rh_g_cingul_post_ventral_area',
    'rh_g_cuneus_area',
    'rh_g_front_inf_opercular_area',
    'rh_g_front_inf_orbital_area',
    'rh_g_front_inf_triangul_area',
    'rh_g_front_middle_area',
    'rh_g_front_sup_area',
    'rh_g_ins_lg_and_s_cent_ins_area',
    'rh_g_insular_short_area',
    'rh_g_occipital_middle_area',
    'rh_g_occipital_sup_area',
    'rh_g_oc_temp_lat_fusifor_area',
    'rh_g_oc_temp_med_lingual_area',
    'rh_g_oc_temp_med_parahip_area',
    'rh_g_orbital_area',
    'rh_g_pariet_inf_angular_area',
    'rh_g_pariet_inf_supramar_area',
    'rh_g_parietal_sup_area',
    'rh_g_postcentral_area',
    'rh_g_precentral_area',
    'rh_g_precuneus_area',
    'rh_g_rectus_area',
    'rh_g_subcallosal_area',
    'rh_g_temp_sup_g_t_transv_area',
    'rh_g_temp_sup_lateral_area',
    'rh_g_temp_sup_plan_polar_area',
    'rh_g_temp_sup_plan_tempo_area',
    'rh_g_temporal_inf_area',
    'rh_g_temporal_middle_area',
    'rh_lat_fis_ant_horizont_area',
    'rh_lat_fis_ant_vertical_area',
    'rh_lat_fis_post_area',
    'rh_pole_occipital_area',
    'rh_pole_temporal_area',
    'rh_s_calcarine_area',
    'rh_s_central_area',
    'rh_s_cingul_marginalis_area',
    'rh_s_circular_insula_ant_area',
    'rh_s_circular_insula_inf_area',
    'rh_s_circular_insula_sup_area',
    'rh_s_collat_transv_ant_area',
    'rh_s_collat_transv_post_area',
    'rh_s_front_inf_area',
    'rh_s_front_middle_area',
    'rh_s_front_sup_area',
    'rh_s_interm_prim_jensen_area',
    'rh_s_intrapariet_and_p_trans_area',
    'rh_s_oc_middle_and_lunatus_area',
    'rh_s_oc_sup_and_transversal_area',
    'rh_s_occipital_ant_area',
    'rh_s_oc_temp_lat_area',
    'rh_s_oc_temp_med_and_lingual_area',
    'rh_s_orbital_lateral_area',
    'rh_s_orbital_med_olfact_area',
    'rh_s_orbital_h_shaped_area',
    'rh_s_parieto_occipital_area',
    'rh_s_pericallosal_area',
    'rh_s_postcentral_area',
    'rh_s_precentral_inf_part_area',
    'rh_s_precentral_sup_part_area',
    'rh_s_suborbital_area',
    'rh_s_subparietal_area',
    'rh_s_temporal_inf_area',
    'rh_s_temporal_sup_area',
    'rh_s_temporal_transverse_area',
    'rh_whitesurfarea_area',
    'lh_g_and_s_frontomargin_volume',
    'lh_g_and_s_occipital_inf_volume',
    'lh_g_and_s_paracentral_volume',
    'lh_g_and_s_subcentral_volume',
    'lh_g_and_s_transv_frontopol_volume',
    'lh_g_and_s_cingul_ant_volume',
    'lh_g_and_s_cingul_mid_ant_volume',
    'lh_g_and_s_cingul_mid_post_volume',
    'lh_g_cingul_post_dorsal_volume',
    'lh_g_cingul_post_ventral_volume',
    'lh_g_cuneus_volume',
    'lh_g_front_inf_opercular_volume',
    'lh_g_front_inf_orbital_volume',
    'lh_g_front_inf_triangul_volume',
    'lh_g_front_middle_volume',
    'lh_g_front_sup_volume',
    'lh_g_ins_lg_and_s_cent_ins_volume',
    'lh_g_insular_short_volume',
    'lh_g_occipital_middle_volume',
    'lh_g_occipital_sup_volume',
    'lh_g_oc_temp_lat_fusifor_volume',
    'lh_g_oc_temp_med_lingual_volume',
    'lh_g_oc_temp_med_parahip_volume',
    'lh_g_orbital_volume',
    'lh_g_pariet_inf_angular_volume',
    'lh_g_pariet_inf_supramar_volume',
    'lh_g_parietal_sup_volume',
    'lh_g_postcentral_volume',
    'lh_g_precentral_volume',
    'lh_g_precuneus_volume',
    'lh_g_rectus_volume',
    'lh_g_subcallosal_volume',
    'lh_g_temp_sup_g_t_transv_volume',
    'lh_g_temp_sup_lateral_volume',
    'lh_g_temp_sup_plan_polar_volume',
    'lh_g_temp_sup_plan_tempo_volume',
    'lh_g_temporal_inf_volume',
    'lh_g_temporal_middle_volume',
    'lh_lat_fis_ant_horizont_volume',
    'lh_lat_fis_ant_vertical_volume',
    'lh_lat_fis_post_volume',
    'lh_pole_occipital_volume',
    'lh_pole_temporal_volume',
    'lh_s_calcarine_volume',
    'lh_s_central_volume',
    'lh_s_cingul_marginalis_volume',
    'lh_s_circular_insula_ant_volume',
    'lh_s_circular_insula_inf_volume',
    'lh_s_circular_insula_sup_volume',
    'lh_s_collat_transv_ant_volume',
    'lh_s_collat_transv_post_volume',
    'lh_s_front_inf_volume',
    'lh_s_front_middle_volume',
    'lh_s_front_sup_volume',
    'lh_s_interm_prim_jensen_volume',
    'lh_s_intrapariet_and_p_trans_volume',
    'lh_s_oc_middle_and_lunatus_volume',
    'lh_s_oc_sup_and_transversal_volume',
    'lh_s_occipital_ant_volume',
    'lh_s_oc_temp_lat_volume',
    'lh_s_oc_temp_med_and_lingual_volume',
    'lh_s_orbital_lateral_volume',
    'lh_s_orbital_med_olfact_volume',
    'lh_s_orbital_h_shaped_volume',
    'lh_s_parieto_occipital_volume',
    'lh_s_pericallosal_volume',
    'lh_s_postcentral_volume',
    'lh_s_precentral_inf_part_volume',
    'lh_s_precentral_sup_part_volume',
    'lh_s_suborbital_volume',
    'lh_s_subparietal_volume',
    'lh_s_temporal_inf_volume',
    'lh_s_temporal_sup_volume',
    'lh_s_temporal_transverse_volume',
    'rh_g_and_s_frontomargin_volume',
    'rh_g_and_s_occipital_inf_volume',
    'rh_g_and_s_paracentral_volume',
    'rh_g_and_s_subcentral_volume',
    'rh_g_and_s_transv_frontopol_volume',
    'rh_g_and_s_cingul_ant_volume',
    'rh_g_and_s_cingul_mid_ant_volume',
    'rh_g_and_s_cingul_mid_post_volume',
    'rh_g_cingul_post_dorsal_volume',
    'rh_g_cingul_post_ventral_volume',
    'rh_g_cuneus_volume',
    'rh_g_front_inf_opercular_volume',
    'rh_g_front_inf_orbital_volume',
    'rh_g_front_inf_triangul_volume',
    'rh_g_front_middle_volume',
    'rh_g_front_sup_volume',
    'rh_g_ins_lg_and_s_cent_ins_volume',
    'rh_g_insular_short_volume',
    'rh_g_occipital_middle_volume',
    'rh_g_occipital_sup_volume',
    'rh_g_oc_temp_lat_fusifor_volume',
    'rh_g_oc_temp_med_lingual_volume',
    'rh_g_oc_temp_med_parahip_volume',
    'rh_g_orbital_volume',
    'rh_g_pariet_inf_angular_volume',
    'rh_g_pariet_inf_supramar_volume',
    'rh_g_parietal_sup_volume',
    'rh_g_postcentral_volume',
    'rh_g_precentral_volume',
    'rh_g_precuneus_volume',
    'rh_g_rectus_volume',
    'rh_g_subcallosal_volume',
    'rh_g_temp_sup_g_t_transv_volume',
    'rh_g_temp_sup_lateral_volume',
    'rh_g_temp_sup_plan_polar_volume',
    'rh_g_temp_sup_plan_tempo_volume',
    'rh_g_temporal_inf_volume',
    'rh_g_temporal_middle_volume',
    'rh_lat_fis_ant_horizont_volume',
    'rh_lat_fis_ant_vertical_volume',
    'rh_lat_fis_post_volume',
    'rh_pole_occipital_volume',
    'rh_pole_temporal_volume',
    'rh_s_calcarine_volume',
    'rh_s_central_volume',
    'rh_s_cingul_marginalis_volume',
    'rh_s_circular_insula_ant_volume',
    'rh_s_circular_insula_inf_volume',
    'rh_s_circular_insula_sup_volume',
    'rh_s_collat_transv_ant_volume',
    'rh_s_collat_transv_post_volume',
    'rh_s_front_inf_volume',
    'rh_s_front_middle_volume',
    'rh_s_front_sup_volume',
    'rh_s_interm_prim_jensen_volume',
    'rh_s_intrapariet_and_p_trans_volume',
    'rh_s_oc_middle_and_lunatus_volume',
    'rh_s_oc_sup_and_transversal_volume',
    'rh_s_occipital_ant_volume',
    'rh_s_oc_temp_lat_volume',
    'rh_s_oc_temp_med_and_lingual_volume',
    'rh_s_orbital_lateral_volume',
    'rh_s_orbital_med_olfact_volume',
    'rh_s_orbital_h_shaped_volume',
    'rh_s_parieto_occipital_volume',
    'rh_s_pericallosal_volume',
    'rh_s_postcentral_volume',
    'rh_s_precentral_inf_part_volume',
    'rh_s_precentral_sup_part_volume',
    'rh_s_suborbital_volume',
    'rh_s_subparietal_volume',
    'rh_s_temporal_inf_volume',
    'rh_s_temporal_sup_volume',
    'rh_s_temporal_transverse_volume',
    'lh_g_and_s_frontomargin_thickness',
    'lh_g_and_s_occipital_inf_thickness',
    'lh_g_and_s_paracentral_thickness',
    'lh_g_and_s_subcentral_thickness',
    'lh_g_and_s_transv_frontopol_thickness',
    'lh_g_and_s_cingul_ant_thickness',
    'lh_g_and_s_cingul_mid_ant_thickness',
    'lh_g_and_s_cingul_mid_post_thickness',
    'lh_g_cingul_post_dorsal_thickness',
    'lh_g_cingul_post_ventral_thickness',
    'lh_g_cuneus_thickness',
    'lh_g_front_inf_opercular_thickness',
    'lh_g_front_inf_orbital_thickness',
    'lh_g_front_inf_triangul_thickness',
    'lh_g_front_middle_thickness',
    'lh_g_front_sup_thickness',
    'lh_g_ins_lg_and_s_cent_ins_thickness',
    'lh_g_insular_short_thickness',
    'lh_g_occipital_middle_thickness',
    'lh_g_occipital_sup_thickness',
    'lh_g_oc_temp_lat_fusifor_thickness',
    'lh_g_oc_temp_med_lingual_thickness',
    'lh_g_oc_temp_med_parahip_thickness',
    'lh_g_orbital_thickness',
    'lh_g_pariet_inf_angular_thickness',
    'lh_g_pariet_inf_supramar_thickness',
    'lh_g_parietal_sup_thickness',
    'lh_g_postcentral_thickness',
    'lh_g_precentral_thickness',
    'lh_g_precuneus_thickness',
    'lh_g_rectus_thickness',
    'lh_g_subcallosal_thickness',
    'lh_g_temp_sup_g_t_transv_thickness',
    'lh_g_temp_sup_lateral_thickness',
    'lh_g_temp_sup_plan_polar_thickness',
    'lh_g_temp_sup_plan_tempo_thickness',
    'lh_g_temporal_inf_thickness',
    'lh_g_temporal_middle_thickness',
    'lh_lat_fis_ant_horizont_thickness',
    'lh_lat_fis_ant_vertical_thickness',
    'lh_lat_fis_post_thickness',
    'lh_pole_occipital_thickness',
    'lh_pole_temporal_thickness',
    'lh_s_calcarine_thickness',
    'lh_s_central_thickness',
    'lh_s_cingul_marginalis_thickness',
    'lh_s_circular_insula_ant_thickness',
    'lh_s_circular_insula_inf_thickness',
    'lh_s_circular_insula_sup_thickness',
    'lh_s_collat_transv_ant_thickness',
    'lh_s_collat_transv_post_thickness',
    'lh_s_front_inf_thickness',
    'lh_s_front_middle_thickness',
    'lh_s_front_sup_thickness',
    'lh_s_interm_prim_jensen_thickness',
    'lh_s_intrapariet_and_p_trans_thickness',
    'lh_s_oc_middle_and_lunatus_thickness',
    'lh_s_oc_sup_and_transversal_thickness',
    'lh_s_occipital_ant_thickness',
    'lh_s_oc_temp_lat_thickness',
    'lh_s_oc_temp_med_and_lingual_thickness',
    'lh_s_orbital_lateral_thickness',
    'lh_s_orbital_med_olfact_thickness',
    'lh_s_orbital_h_shaped_thickness',
    'lh_s_parieto_occipital_thickness',
    'lh_s_pericallosal_thickness',
    'lh_s_postcentral_thickness',
    'lh_s_precentral_inf_part_thickness',
    'lh_s_precentral_sup_part_thickness',
    'lh_s_suborbital_thickness',
    'lh_s_subparietal_thickness',
    'lh_s_temporal_inf_thickness',
    'lh_s_temporal_sup_thickness',
    'lh_s_temporal_transverse_thickness',
    'lh_meanthickness_thickness',
    'rh_g_and_s_frontomargin_thickness',
    'rh_g_and_s_occipital_inf_thickness',
    'rh_g_and_s_paracentral_thickness',
    'rh_g_and_s_subcentral_thickness',
    'rh_g_and_s_transv_frontopol_thickness',
    'rh_g_and_s_cingul_ant_thickness',
    'rh_g_and_s_cingul_mid_ant_thickness',
    'rh_g_and_s_cingul_mid_post_thickness',
    'rh_g_cingul_post_dorsal_thickness',
    'rh_g_cingul_post_ventral_thickness',
    'rh_g_cuneus_thickness',
    'rh_g_front_inf_opercular_thickness',
    'rh_g_front_inf_orbital_thickness',
    'rh_g_front_inf_triangul_thickness',
    'rh_g_front_middle_thickness',
    'rh_g_front_sup_thickness',
    'rh_g_ins_lg_and_s_cent_ins_thickness',
    'rh_g_insular_short_thickness',
    'rh_g_occipital_middle_thickness',
    'rh_g_occipital_sup_thickness',
    'rh_g_oc_temp_lat_fusifor_thickness',
    'rh_g_oc_temp_med_lingual_thickness',
    'rh_g_oc_temp_med_parahip_thickness',
    'rh_g_orbital_thickness',
    'rh_g_pariet_inf_angular_thickness',
    'rh_g_pariet_inf_supramar_thickness',
    'rh_g_parietal_sup_thickness',
    'rh_g_postcentral_thickness',
    'rh_g_precentral_thickness',
    'rh_g_precuneus_thickness',
    'rh_g_rectus_thickness',
    'rh_g_subcallosal_thickness',
    'rh_g_temp_sup_g_t_transv_thickness',
    'rh_g_temp_sup_lateral_thickness',
    'rh_g_temp_sup_plan_polar_thickness',
    'rh_g_temp_sup_plan_tempo_thickness',
    'rh_g_temporal_inf_thickness',
    'rh_g_temporal_middle_thickness',
    'rh_lat_fis_ant_horizont_thickness',
    'rh_lat_fis_ant_vertical_thickness',
    'rh_lat_fis_post_thickness',
    'rh_pole_occipital_thickness',
    'rh_pole_temporal_thickness',
    'rh_s_calcarine_thickness',
    'rh_s_central_thickness',
    'rh_s_cingul_marginalis_thickness',
    'rh_s_circular_insula_ant_thickness',
    'rh_s_circular_insula_inf_thickness',
    'rh_s_circular_insula_sup_thickness',
    'rh_s_collat_transv_ant_thickness',
    'rh_s_collat_transv_post_thickness',
    'rh_s_front_inf_thickness',
    'rh_s_front_middle_thickness',
    'rh_s_front_sup_thickness',
    'rh_s_interm_prim_jensen_thickness',
    'rh_s_intrapariet_and_p_trans_thickness',
    'rh_s_oc_middle_and_lunatus_thickness',
    'rh_s_oc_sup_and_transversal_thickness',
    'rh_s_occipital_ant_thickness',
    'rh_s_oc_temp_lat_thickness',
    'rh_s_oc_temp_med_and_lingual_thickness',
    'rh_s_orbital_lateral_thickness',
    'rh_s_orbital_med_olfact_thickness',
    'rh_s_orbital_h_shaped_thickness',
    'rh_s_parieto_occipital_thickness',
    'rh_s_pericallosal_thickness',
    'rh_s_postcentral_thickness',
    'rh_s_precentral_inf_part_thickness',
    'rh_s_precentral_sup_part_thickness',
    'rh_s_suborbital_thickness',
    'rh_s_subparietal_thickness',
    'rh_s_temporal_inf_thickness',
    'rh_s_temporal_sup_thickness',
    'rh_s_temporal_transverse_thickness',
    'rh_meanthickness_thickness',
    'brainsegvolnotvent',
    'etiv',
    ]
vals = list()
for roi in rois:
    mask = [x==roi for x in aparc.columns]
    if sum(mask)==0:
        print(f'  WARNING - no volume found for ROI {roi}')
        vals.append(0)
    elif sum(mask)>1:
        raise Exception(f'Found >1 value for {roi}')
    else:
        vals.append(aparc[roi].array[0])


# Make data frame and write to file
aparcout = pandas.DataFrame([rois, vals])
os.makedirs(args.out_dir, exist_ok=True)
aparcout.to_csv(os.path.join(args.out_dir,'a2009s.csv'), 
    header=False, index=False)
