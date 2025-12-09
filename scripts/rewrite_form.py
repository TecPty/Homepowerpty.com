@"
from pathlib import Path
import re

# Reemplazar sección completa de formularios en index.html
html_path = Path("index.html")
html = html_path.read_text(encoding="utf-8")

new_forms = """<section class="section_forms" id="contacto">
            <div class="forms_container">
                <!-- Formulario de contacto -->
                <div class="form_wrapper contact_wrapper">
                    <h2 class="form_title">Resolvemos tus inquietudes</h2>
                    
                    <form class="contact_form" id="form">
                        <input type="hidden" name="form_type" value="contact">
                        <div class="form_item">
                            <input type="text" class="form_input" name="name" id="contact_name">
                            <label for="contact_name" class="form_label">Nombre</label>
                        </div>
                        <div class="form_item">
                            <input type="text" class="form_input" name="number" id="contact_number">
                            <label for="contact_number" class="form_label">Teléfono</label>
                        </div>
                        <div class="form_item">
                            <input type="email" class="form_input" name="email" id="contact_email">
                            <label for="contact_email" class="form_label">Correo electrónico</label>
                        </div>
                        <div class="form_item">
                            <input type="text" class="form_input" name="company" id="contact_company">
                            <label for="contact_company" class="form_label">Empresa</label>
                        </div>
                        <div class="form_item">
                            <textarea class="form_input form_textarea" name="message" id="contact_message"></textarea>
                            <label for="contact_message" class="form_label">Mensaje</label>
                        </div>
                        <div class="form_item">
                            <p class="form_msg" id="form_msg"></p>
                        </div>
                        <div class="form_item">
                            <input type="submit" class="form_input form_submit" value="Contactar">
                        </div>
                    </form>
                </div>

                <!-- Formulario de Empleo -->
                <div class="form_wrapper careers_wrapper">
                    <h2 class="form_title">Oportunidades de Empleo</h2>
                    <p class="form_subtitle">
                        ¿Te gustaría formar parte del equipo de Home Power? Envíanos tu información y nos pondremos en contacto contigo.
                            </p>
                    
                    <form class="careers_form" id="careers_form">
                        <input type="hidden" name="form_type" value="careers">
                        <div class="form_item">
                            <input type="text" class="form_input" name="full_name" id="careers_name" required>
                            <label for="careers_name" class="form_label">Nombre completo</label>
                        </div>
                        <div class="form_item">
                            <input type="email" class="form_input" name="email" id="careers_email" required>
                            <label for="careers_email" class="form_label">Correo electrónico</label>
                        </div>
                        <div class="form_item">
                            <input type="tel" class="form_input" name="phone" id="careers_phone" required>
                            <label for="careers_phone" class="form_label">Teléfono</label>
                        </div>
                        <div class="form_item">
                            <select class="form_input form_select" name="position" id="careers_position" required>
                                <option value="" disabled selected></option>
                                <option value="vendedor">Vendedor/a</option>
                                <option value="administracion">Administración</option>
                                <option value="logistica">Logística y Almacén</option>
                                <option value="marketing">Marketing Digital</option>
                                <option value="contabilidad">Contabilidad</option>
                                <option value="otro">Otro</option>
                            </select>
                            <label for="careers_position" class="form_label">Posición de interés</label>
                        </div>
                        <div class="form_item">
                            <textarea class="form_input form_textarea" name="experience" id="careers_experience" rows="4"></textarea>
                            <label for="careers_experience" class="form_label">Experiencia laboral relevante</label>
                        </div>
                        <div class="form_item file_actions">
                            <input type="file" id="cv_file" name="cv_file" accept=".pdf,.doc,.docx" hidden>
                            <button type="button" class="file_button" id="cv_trigger">Adjuntar CV (PDF/Word)</button>
                            <span class="file_name" id="file_name">Ningún archivo seleccionado</span>
                        </div>
                        <div class="form_item">
                            <p class="form_msg" id="careers_form_msg"></p>
                        </div>
                        <div class="form_item">
                            <input type="submit" class="form_input form_submit careers_submit" value="Enviar Aplicación">
                        </div>
                    </form>
                </div>
            </div>
        </section>"""

html = re.sub(r'<section class="section_forms".*?</section>', new_forms, html, count=1, flags=re.S)
html_path.write_text(html, encoding="utf-8")

# Ajustar JS careers: quitar motivación
js_path = Path('scripts/send_careers_form.js')
js = js_path.read_text(encoding='utf-8')
js = js.replace("case 'motivation':\n                return value.trim().length >= 20;\n", "")
js = js.replace("const experience = formData.get('experience')?.trim();\n        const motivation = formData.get('motivation')?.trim();\n",
                "const experience = formData.get('experience')?.trim();\n")
js = js.replace("||\n            !validateField('position', position) ||\n            !validateField('motivation', motivation)",
                "||\n            !validateField('position', position)")
js = js.replace('La motivaci¢n debe tener al menos 20 caracteres.', '')
js = js.replace('Enviar Aplicaci¢n', 'Enviar Aplicación')
js_path.write_text(js, encoding='utf-8')

# Ajustar PHP: quitar motivación en careers
php_path = Path('php/send_form.php')
php = php_path.read_text(encoding='utf-8')
php = re.sub(r"\\$motivation= trim\\(\\(string\\)filter_input\\(INPUT_POST, 'motivation'.*?;\\n", "", php)
php = re.sub(r"if \\(strlen\\(\\$full_name\\) < 2 .*?\\$position\\) < 2\\) \\{\\s*echo json_encode\\('invalid'\\);\\s*exit;\\s*\\}\\n",
             "if (strlen($full_name) < 2 || !filter_var($email, FILTER_VALIDATE_EMAIL) || !valid_phone($phone) || strlen($position) < 2) {\n        echo json_encode('invalid');\n        exit;\n    }\n",
             php, flags=re.S)
php = php.replace("<p><strong>Motivación:</strong></p><div style=\"background:#fff;padding:10px;border-left:4px solid #FF9F1C;\">' . nl2br(htmlspecialchars($motivation, ENT_QUOTES, 'UTF-8')) . '</div>' .\n        \"</div><hr style='border:1px solid #eee;margin:20px 0;'><p style='font-size:12px;color:#666;text-align:center;'>Enviado desde: \" . htmlspecialchars($_SERVER['HTTP_HOST'] ?? 'cli', ENT_QUOTES, 'UTF-8') . ' el ' . date('d/m/Y H:i:s') . \"</p></div></body></html>\";",
                      "\"</div><hr style='border:1px solid #eee;margin:20px 0;'><p style='font-size:12px;color:#666;text-align:center;'>Enviado desde: \" . htmlspecialchars($_SERVER['HTTP_HOST'] ?? 'cli', ENT_QUOTES, 'UTF-8') . ' el ' . date('d/m/Y H:i:s') . \"</p></div></body></html>\";")
php_path.write_text(php, encoding='utf-8')

print("Reemplazo completado")
"@ | Set-Content rewrite_forms.py
python rewrite_forms.py"}
