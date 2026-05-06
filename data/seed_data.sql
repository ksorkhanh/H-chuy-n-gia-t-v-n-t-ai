-- ============================================================
-- Legal Expert System - Seed Data
-- Vietnamese Land Law 2024 sample data
-- ============================================================

-- ============================================================
-- 1. Default Users (password = '123456' for all)
-- ============================================================
-- Password hash for '123456' with salt 'default_salt_admin'
INSERT INTO users (username, password_hash, salt, role, full_name, email) VALUES
('admin', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'default_salt_admin', 'admin', 'Quản trị viên', 'admin@legal.vn'),
('staff01', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'default_salt_staff', 'staff', 'Nguyễn Văn A', 'staff01@legal.vn'),
('expert01', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'default_salt_expert', 'expert', 'TS. Trần Thị B', 'expert01@legal.vn');

-- ============================================================
-- 2. Permissions
-- ============================================================
INSERT INTO permissions (name, description) VALUES
('manage_legal', 'Quản lý văn bản pháp lý'),
('manage_rules', 'Quản lý luật suy diễn'),
('manage_users', 'Quản lý người dùng'),
('run_consultation', 'Thực hiện tư vấn'),
('view_results', 'Xem kết quả tư vấn'),
('view_history', 'Xem lịch sử tư vấn'),
('import_export', 'Import/Export dữ liệu'),
('propose_rules', 'Đề xuất luật mới');

-- Admin permissions
INSERT INTO role_permissions (role, permission_id) VALUES
('admin', 1), ('admin', 2), ('admin', 3), ('admin', 4),
('admin', 5), ('admin', 6), ('admin', 7);

-- Staff permissions
INSERT INTO role_permissions (role, permission_id) VALUES
('staff', 4), ('staff', 5), ('staff', 6);

-- Expert permissions
INSERT INTO role_permissions (role, permission_id) VALUES
('expert', 4), ('expert', 5), ('expert', 6), ('expert', 8), ('expert', 2);

-- ============================================================
-- 3. Legal Documents
-- ============================================================
INSERT INTO legal_documents (title, code, year, domain, description) VALUES
('Luật Đất đai 2024', 'LUAT_DD_2024', 2024, 'dat_dai', 'Luật Đất đai số 31/2024/QH15 được Quốc hội thông qua ngày 18/01/2024, có hiệu lực từ 01/01/2025'),
('Nghị định 88/2024/NĐ-CP', 'ND_88_2024', 2024, 'dat_dai', 'Nghị định quy định về bồi thường, hỗ trợ, tái định cư khi Nhà nước thu hồi đất'),
('Nghị định 91/2019/NĐ-CP', 'ND_91_2019', 2019, 'dat_dai', 'Nghị định về xử phạt vi phạm hành chính trong lĩnh vực đất đai'),
('Luật Công chứng 2014', 'LUAT_CC_2014', 2014, 'dat_dai', 'Luật Công chứng số 53/2014/QH13 quy định về công chứng hợp đồng, giao dịch');

-- ============================================================
-- 4. Legal Articles - Module: Chuyển nhượng (transfer)
-- ============================================================
INSERT INTO legal_articles (document_id, article_number, clause, content, keywords) VALUES
-- Luật Đất đai 2024
(1, 'Điều 45', 'Khoản 1', 'Người sử dụng đất được thực hiện quyền chuyển nhượng quyền sử dụng đất khi có Giấy chứng nhận quyền sử dụng đất, quyền sở hữu tài sản gắn liền với đất; đất không có tranh chấp; quyền sử dụng đất không bị kê biên để bảo đảm thi hành án; trong thời hạn sử dụng đất.', 'chuyển nhượng, giấy chứng nhận, điều kiện, tranh chấp'),
(1, 'Điều 45', 'Khoản 2', 'Ngoài các điều kiện quy định tại khoản 1 Điều này, người sử dụng đất khi thực hiện các quyền chuyển nhượng phải đáp ứng các điều kiện theo quy định tại các điều từ Điều 46 đến Điều 50 của Luật này.', 'chuyển nhượng, điều kiện bổ sung'),
(1, 'Điều 27', NULL, 'Nhà nước công nhận quyền sử dụng đất thông qua việc cấp Giấy chứng nhận quyền sử dụng đất, quyền sở hữu tài sản gắn liền với đất cho người đang sử dụng đất ổn định.', 'giấy chứng nhận, công nhận, quyền sử dụng đất'),
(1, 'Điều 153', NULL, 'Hợp đồng chuyển nhượng quyền sử dụng đất phải được công chứng hoặc chứng thực, trừ trường hợp một bên là tổ chức kinh doanh bất động sản.', 'hợp đồng, công chứng, chứng thực, chuyển nhượng'),
(1, 'Điều 155', NULL, 'Người chuyển nhượng quyền sử dụng đất phải thực hiện nghĩa vụ tài chính gồm thuế thu nhập cá nhân, phí, lệ phí theo quy định của pháp luật.', 'nghĩa vụ tài chính, thuế, phí, lệ phí');

-- ============================================================
-- 5. Legal Articles - Module: Bồi thường (compensation)
-- ============================================================
INSERT INTO legal_articles (document_id, article_number, clause, content, keywords) VALUES
(1, 'Điều 79', 'Khoản 1', 'Nhà nước thu hồi đất trong các trường hợp: Để thực hiện dự án phát triển kinh tế - xã hội vì lợi ích quốc gia, công cộng; Để thực hiện các dự án tạo quỹ đất theo quy hoạch.', 'thu hồi đất, lợi ích quốc gia, phát triển kinh tế'),
(1, 'Điều 91', NULL, 'Nguyên tắc bồi thường khi Nhà nước thu hồi đất: Bồi thường bằng đất có cùng mục đích sử dụng hoặc bằng tiền theo giá đất cụ thể tại thời điểm có quyết định thu hồi đất.', 'bồi thường, nguyên tắc, giá đất, thu hồi'),
(1, 'Điều 95', NULL, 'Điều kiện được bồi thường về đất khi Nhà nước thu hồi đất: có Giấy chứng nhận hoặc đủ điều kiện cấp Giấy chứng nhận; đất không thuộc trường hợp giao không thu tiền sử dụng đất.', 'điều kiện bồi thường, giấy chứng nhận'),
(2, 'Điều 5', NULL, 'Giá đất cụ thể để tính bồi thường khi Nhà nước thu hồi đất được xác định theo phương pháp định giá đất quy định tại Luật Đất đai, phù hợp với giá đất phổ biến trên thị trường.', 'giá đất cụ thể, bồi thường, phương pháp định giá'),
(2, 'Điều 15', NULL, 'Hỗ trợ tái định cư: Hộ gia đình, cá nhân khi Nhà nước thu hồi đất ở mà phải di chuyển chỗ ở, nếu không có chỗ ở nào khác trong địa bàn xã, phường, thị trấn nơi có đất thu hồi thì được bố trí tái định cư.', 'hỗ trợ, tái định cư, thu hồi đất ở');

-- ============================================================
-- 6. Legal Articles - Module: Vi phạm (violation)
-- ============================================================
INSERT INTO legal_articles (document_id, article_number, clause, content, keywords) VALUES
(3, 'Điều 9', NULL, 'Sử dụng đất lấn, chiếm: Phạt tiền từ 1.000.000 đồng đến 3.000.000 đồng đối với trường hợp lấn, chiếm đất chưa sử dụng có diện tích dưới 0,02 hecta tại khu vực nông thôn.', 'lấn chiếm, phạt tiền, đất chưa sử dụng, nông thôn'),
(3, 'Điều 10', NULL, 'Sử dụng đất không đúng mục đích: Phạt tiền từ 2.000.000 đồng đến 5.000.000 đồng khi chuyển mục đích sử dụng đất trồng lúa sang đất trồng cây lâu năm mà không được phép.', 'không đúng mục đích, chuyển mục đích, đất trồng lúa'),
(3, 'Điều 14', NULL, 'Tự ý chuyển nhượng quyền sử dụng đất dưới hình thức phân lô, bán nền mà không đủ điều kiện theo quy định: Phạt tiền từ 20.000.000 đồng đến 50.000.000 đồng.', 'phân lô bán nền, chuyển nhượng trái phép'),
(3, 'Điều 6', 'Khoản 1', 'Tình tiết tăng nặng: Vi phạm nhiều lần; tái phạm; vi phạm với diện tích lớn; gây hậu quả nghiêm trọng; không chấp hành quyết định xử phạt.', 'tăng nặng, tái phạm, hậu quả nghiêm trọng'),
(3, 'Điều 7', NULL, 'Biện pháp khắc phục hậu quả: Buộc khôi phục lại tình trạng ban đầu của đất trước khi vi phạm; buộc nộp lại số lợi bất hợp pháp có được do thực hiện hành vi vi phạm.', 'khắc phục, khôi phục, nộp lại, lợi bất hợp pháp');

-- ============================================================
-- 7. Legal Relations
-- ============================================================
INSERT INTO legal_relations (source_article_id, related_article_id, relation_type) VALUES
(1, 2, 'supplement'),    -- Điều 45 K1 <-> K2
(1, 3, 'reference'),     -- Điều 45 -> Điều 27 (giấy CN)
(1, 4, 'reference'),     -- Điều 45 -> Điều 153 (công chứng)
(4, 5, 'supplement'),    -- Điều 153 -> Điều 155 (nghĩa vụ TC)
(6, 7, 'detail'),        -- Điều 79 -> Điều 91 (nguyên tắc BT)
(7, 8, 'supplement'),    -- Điều 91 -> Điều 95 (điều kiện BT)
(7, 9, 'detail'),        -- Điều 91 -> NĐ88 Điều 5 (giá đất)
(8, 10, 'supplement');   -- Điều 95 -> NĐ88 Điều 15 (tái định cư)

-- ============================================================
-- 8. Fuzzy Rules - Module: Transfer (Chuyển nhượng QSD đất)
-- ============================================================
INSERT INTO rules (module, name, condition_json, conclusion, weight, legal_article_id, description) VALUES
-- Nếu tính pháp lý tốt VÀ giá trị phù hợp → Khả thi cao
('transfer', 'R1_Transfer_High', '[{"variable":"legal_status","term":"complete"},{"variable":"land_value","term":"reasonable"}]', 'high_feasibility', 1.0, 1, 'Giấy tờ đầy đủ, giá hợp lý → Khả thi cao'),
('transfer', 'R2_Transfer_High2', '[{"variable":"legal_status","term":"complete"},{"variable":"area","term":"medium"},{"variable":"financial_obligation","term":"fulfilled"}]', 'high_feasibility', 0.9, 4, 'Pháp lý đầy đủ, diện tích vừa, đã nộp thuế → Khả thi cao'),
-- Nếu tính pháp lý trung bình → Khả thi trung bình
('transfer', 'R3_Transfer_Medium', '[{"variable":"legal_status","term":"partial"},{"variable":"land_value","term":"reasonable"}]', 'medium_feasibility', 0.8, 2, 'Giấy tờ chưa đầy đủ, giá hợp lý → Cần bổ sung hồ sơ'),
('transfer', 'R4_Transfer_Medium2', '[{"variable":"legal_status","term":"complete"},{"variable":"land_value","term":"high"},{"variable":"location","term":"rural"}]', 'medium_feasibility', 0.7, 5, 'Pháp lý đầy đủ nhưng giá cao, vùng nông thôn → Cân nhắc'),
-- Nếu pháp lý kém → Khả thi thấp
('transfer', 'R5_Transfer_Low', '[{"variable":"legal_status","term":"incomplete"},{"variable":"land_value","term":"high"}]', 'low_feasibility', 1.0, 1, 'Không đủ giấy tờ → Không thể chuyển nhượng'),
('transfer', 'R6_Transfer_Low2', '[{"variable":"legal_status","term":"incomplete"},{"variable":"financial_obligation","term":"unfulfilled"}]', 'low_feasibility', 0.9, 5, 'Thiếu pháp lý và chưa nộp thuế → Rủi ro cao');

-- ============================================================
-- 9. Fuzzy Rules - Module: Compensation (Bồi thường thu hồi đất)
-- ============================================================
INSERT INTO rules (module, name, condition_json, conclusion, weight, legal_article_id, description) VALUES
-- Bồi thường cao
('compensation', 'R1_Comp_High', '[{"variable":"land_type","term":"residential"},{"variable":"usage_duration","term":"long"},{"variable":"area","term":"large"}]', 'high_compensation', 1.0, 7, 'Đất ở, sử dụng lâu, diện tích lớn → Bồi thường cao'),
('compensation', 'R2_Comp_High2', '[{"variable":"land_type","term":"residential"},{"variable":"k_coefficient","term":"high"},{"variable":"resettlement","term":"needed"}]', 'high_compensation', 0.9, 10, 'Đất ở, hệ số K cao, cần tái định cư → Bồi thường cao'),
-- Bồi thường trung bình
('compensation', 'R3_Comp_Medium', '[{"variable":"land_type","term":"agricultural"},{"variable":"usage_duration","term":"medium"},{"variable":"area","term":"medium"}]', 'medium_compensation', 0.8, 8, 'Đất nông nghiệp, sử dụng trung bình → Bồi thường vừa'),
('compensation', 'R4_Comp_Medium2', '[{"variable":"land_type","term":"residential"},{"variable":"usage_duration","term":"short"},{"variable":"k_coefficient","term":"medium"}]', 'medium_compensation', 0.7, 9, 'Đất ở, mới sử dụng, hệ số K trung bình'),
-- Bồi thường thấp
('compensation', 'R5_Comp_Low', '[{"variable":"land_type","term":"agricultural"},{"variable":"usage_duration","term":"short"},{"variable":"area","term":"small"}]', 'low_compensation', 1.0, 8, 'Đất nông nghiệp, sử dụng ngắn, diện tích nhỏ → Bồi thường thấp'),
('compensation', 'R6_Comp_Low2', '[{"variable":"land_type","term":"unused"},{"variable":"usage_duration","term":"short"}]', 'low_compensation', 0.9, 6, 'Đất chưa sử dụng, thời gian ngắn → Bồi thường thấp');

-- ============================================================
-- 10. Fuzzy Rules - Module: Violation (Vi phạm hành chính đất đai)
-- ============================================================
INSERT INTO rules (module, name, condition_json, conclusion, weight, legal_article_id, description) VALUES
-- Mức xử phạt nặng
('violation', 'R1_Viol_Heavy', '[{"variable":"severity","term":"serious"},{"variable":"violation_area","term":"large"},{"variable":"recidivism","term":"yes"}]', 'heavy_penalty', 1.0, 14, 'Vi phạm nghiêm trọng, diện tích lớn, tái phạm → Phạt nặng'),
('violation', 'R2_Viol_Heavy2', '[{"variable":"severity","term":"serious"},{"variable":"damage","term":"high"}]', 'heavy_penalty', 0.9, 15, 'Vi phạm nghiêm trọng, thiệt hại lớn → Phạt nặng + khắc phục'),
-- Mức xử phạt trung bình
('violation', 'R3_Viol_Medium', '[{"variable":"severity","term":"moderate"},{"variable":"violation_area","term":"medium"},{"variable":"recidivism","term":"no"}]', 'medium_penalty', 0.8, 11, 'Vi phạm vừa, diện tích vừa, lần đầu → Phạt trung bình'),
('violation', 'R4_Viol_Medium2', '[{"variable":"severity","term":"moderate"},{"variable":"duration","term":"medium"},{"variable":"damage","term":"medium"}]', 'medium_penalty', 0.7, 12, 'Vi phạm vừa, thời gian vừa → Phạt trung bình'),
-- Mức xử phạt nhẹ
('violation', 'R5_Viol_Light', '[{"variable":"severity","term":"minor"},{"variable":"violation_area","term":"small"},{"variable":"recidivism","term":"no"}]', 'light_penalty', 1.0, 11, 'Vi phạm nhẹ, diện tích nhỏ, lần đầu → Phạt nhẹ/cảnh cáo'),
('violation', 'R6_Viol_Light2', '[{"variable":"severity","term":"minor"},{"variable":"damage","term":"low"}]', 'light_penalty', 0.9, 12, 'Vi phạm nhẹ, thiệt hại thấp → Phạt nhẹ');
