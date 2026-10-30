package com.greenair.industrial.qc;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.ClipData;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Base64;
import android.util.Log;
import android.webkit.ConsoleMessage;
import android.webkit.JavascriptInterface;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;
import androidx.activity.ComponentActivity;
import androidx.annotation.Nullable;
import androidx.core.content.FileProvider;
import androidx.webkit.WebViewAssetLoader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.OutputStream;
import org.json.JSONObject;

public class MainActivity extends ComponentActivity {
    private static final String TAG = "GreenAirQC";
    private static final String URL = "https://appassets.androidplatform.net/assets/public/index.html";
    private static final int PICK_PHOTO = 200;
    private static final int SAVE_PDF = 201;
    private WebView webView;
    private ValueCallback<Uri[]> pendingPhotos;
    private Uri cameraOutput;
    private byte[] pdfToSave;
    private String pdfNameToSave;

    @SuppressLint("SetJavaScriptEnabled")
    @Override protected void onCreate(Bundle state) {
        super.onCreate(state);
        webView = new WebView(this);
        setContentView(webView);
        WebSettings cfg = webView.getSettings();
        cfg.setJavaScriptEnabled(true);
        cfg.setDomStorageEnabled(true);
        cfg.setAllowFileAccess(false);
        cfg.setAllowFileAccessFromFileURLs(false);
        cfg.setAllowUniversalAccessFromFileURLs(false);
        cfg.setAllowContentAccess(true);
        cfg.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);

        WebViewAssetLoader loader = new WebViewAssetLoader.Builder()
            .addPathHandler("/assets/", new WebViewAssetLoader.AssetsPathHandler(this))
            .build();
        webView.setWebViewClient(new WebViewClient() {
            @Override public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                return loader.shouldInterceptRequest(request.getUrl());
            }
            @Override public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                Uri url = request.getUrl();
                if ("appassets.androidplatform.net".equals(url.getHost())) return false;
                try { startActivity(new Intent(Intent.ACTION_VIEW, url)); }
                catch (Exception ex) { Log.w(TAG, "No se puede abrir enlace externo", ex); }
                return true;
            }
        });
        webView.setWebChromeClient(new WebChromeClient() {
            @Override public boolean onConsoleMessage(ConsoleMessage msg) {
                if ((getApplicationInfo().flags & android.content.pm.ApplicationInfo.FLAG_DEBUGGABLE) != 0) Log.d(TAG, "JS " + msg.messageLevel() + ": " + msg.message());
                return true;
            }
            @Override public boolean onShowFileChooser(WebView view, ValueCallback<Uri[]> callback, FileChooserParams params) {
                if (pendingPhotos != null) pendingPhotos.onReceiveValue(null);
                pendingPhotos = callback;
                cameraOutput = null;
                try {
                    if (params.isCaptureEnabled()) {
                        Intent camera = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                        File folder = new File(getCacheDir(), "camera");
                        if (!folder.exists() && !folder.mkdirs()) throw new IllegalStateException("No se creó directorio de cámara");
                        File photo = File.createTempFile("qc_photo_", ".jpg", folder);
                        cameraOutput = FileProvider.getUriForFile(MainActivity.this, getPackageName() + ".files", photo);
                        camera.putExtra(MediaStore.EXTRA_OUTPUT, cameraOutput);
                        camera.setClipData(ClipData.newRawUri("Fotografía", cameraOutput));
                        camera.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_WRITE_URI_PERMISSION);
                        startActivityForResult(camera, PICK_PHOTO);
                    } else {
                        Intent pick = new Intent(Intent.ACTION_GET_CONTENT);
                        pick.addCategory(Intent.CATEGORY_OPENABLE);
                        pick.setType("image/*");
                        pick.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, params.getMode() == FileChooserParams.MODE_OPEN_MULTIPLE);
                        startActivityForResult(Intent.createChooser(pick, "Seleccionar fotografías"), PICK_PHOTO);
                    }
                    return true;
                } catch (Exception ex) {
                    Log.e(TAG, "No se pudo abrir cámara o galería", ex);
                    callback.onReceiveValue(null);
                    pendingPhotos = null;
                    cameraOutput = null;
                    Toast.makeText(MainActivity.this, "No se pudo abrir cámara o archivos", Toast.LENGTH_LONG).show();
                    return true;
                }
            }
        });
        // Only bundled page receives the native API. Never enable universal file-origin access.
        webView.addJavascriptInterface(new NativeBridge(), "GreenAirNative");
        webView.loadUrl(URL);
    }

    private String safeName(String name) {
        String value = name == null ? "Ficha_GreenAir.pdf" : name.replaceAll("[^a-zA-Z0-9._-]", "_");
        if (!value.endsWith(".pdf")) value += ".pdf";
        return value.length() > 160 ? value.substring(0, 156) + ".pdf" : value;
    }

    private void notifyJavascript(String action, boolean success, String message) {
        runOnUiThread(() -> {
            String js = "window.dispatchEvent(new CustomEvent('greenair:native-status',{detail:{action:"
                + JSONObject.quote(action) + ",success:" + success + ",message:" + JSONObject.quote(message) + "}}))";
            webView.evaluateJavascript(js, null);
            Toast.makeText(MainActivity.this, message, Toast.LENGTH_LONG).show();
        });
    }

    private final class NativeBridge {
        @JavascriptInterface public void sharePdf(String base64, String name, String summary, String preferred) {
            new Thread(() -> {
                try {
                    byte[] bytes = Base64.decode(base64, Base64.DEFAULT);
                    if (bytes.length < 5 || bytes[0] != '%' || bytes[1] != 'P' || bytes[2] != 'D' || bytes[3] != 'F') throw new IllegalArgumentException("Archivo PDF inválido");
                    File dir = new File(getCacheDir(), "shared_pdfs");
                    if (!dir.exists() && !dir.mkdirs()) throw new IllegalStateException("No se pudo crear almacenamiento temporal");
                    File file = new File(dir, safeName(name));
                    try (FileOutputStream stream = new FileOutputStream(file)) { stream.write(bytes); }
                    Uri uri = FileProvider.getUriForFile(MainActivity.this, getPackageName() + ".files", file);
                    runOnUiThread(() -> {
                        try {
                            Intent intent = new Intent(Intent.ACTION_SEND);
                            intent.setType("application/pdf");
                            intent.putExtra(Intent.EXTRA_STREAM, uri);
                            intent.putExtra(Intent.EXTRA_TEXT, summary);
                            intent.setClipData(ClipData.newRawUri("GreenAir PDF", uri));
                            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
                            // WhatsApp sometimes discards EXTRA_TEXT with PDF; OS/provider decides.
                            if ("whatsapp".equals(preferred)) intent.setPackage("com.whatsapp");
                            try {
                                startActivity(Intent.createChooser(intent, "Compartir ficha PDF"));
                            } catch (Exception whatsappUnavailable) {
                                intent.setPackage(null);
                                startActivity(Intent.createChooser(intent, "Compartir ficha PDF"));
                            }
                            notifyJavascript("share", true, "PDF enviado al selector; confirma el envío en la otra aplicación.");
                        } catch (Exception ex) {
                            Log.e(TAG, "No se pudo compartir PDF", ex);
                            notifyJavascript("share", false, "No se pudo abrir el selector de aplicaciones.");
                        }
                    });
                } catch (Exception ex) {
                    Log.e(TAG, "No se pudo preparar PDF", ex);
                    notifyJavascript("share", false, "No se pudo preparar el documento PDF.");
                }
            }).start();
        }

        @JavascriptInterface public void savePdf(String base64, String name) {
            new Thread(() -> {
                try {
                    byte[] bytes = Base64.decode(base64, Base64.DEFAULT);
                    if (bytes.length < 5 || bytes[0] != '%' || bytes[1] != 'P' || bytes[2] != 'D' || bytes[3] != 'F') throw new IllegalArgumentException("PDF inválido");
                    runOnUiThread(() -> {
                        pdfToSave = bytes;
                        pdfNameToSave = safeName(name);
                        Intent save = new Intent(Intent.ACTION_CREATE_DOCUMENT);
                        save.addCategory(Intent.CATEGORY_OPENABLE);
                        save.setType("application/pdf");
                        save.putExtra(Intent.EXTRA_TITLE, pdfNameToSave);
                        try { startActivityForResult(save, SAVE_PDF); }
                        catch (Exception e) {
                            pdfToSave = null;
                            notifyJavascript("save", false, "No se pudo abrir el selector para guardar.");
                        }
                    });
                } catch (Exception ex) {
                    notifyJavascript("save", false, "No se pudo preparar el PDF para guardar.");
                }
            }).start();
        }
    }

    @Override protected void onActivityResult(int code, int result, @Nullable Intent data) {
        super.onActivityResult(code, result, data);
        if (code == PICK_PHOTO) {
            if (pendingPhotos == null) return;
            Uri[] files = null;
            if (result == Activity.RESULT_OK) {
                if (data != null && data.getClipData() != null) {
                    ClipData clips = data.getClipData();
                    files = new Uri[clips.getItemCount()];
                    for (int i = 0; i < clips.getItemCount(); i++) files[i] = clips.getItemAt(i).getUri();
                } else if (data != null && data.getData() != null) {
                    files = new Uri[]{ data.getData() };
                } else if (cameraOutput != null) {
                    files = new Uri[]{ cameraOutput };
                }
            }
            pendingPhotos.onReceiveValue(files);
            pendingPhotos = null;
            cameraOutput = null;
        }
        if (code == SAVE_PDF) {
            byte[] bytes = pdfToSave;
            pdfToSave = null;
            if (result == Activity.RESULT_OK && data != null && data.getData() != null && bytes != null) {
                try (OutputStream stream = getContentResolver().openOutputStream(data.getData())) {
                    if (stream == null) throw new IllegalStateException("Destino inaccesible");
                    stream.write(bytes);
                    stream.flush();
                    notifyJavascript("save", true, "PDF guardado correctamente.");
                } catch (Exception ex) {
                    Log.e(TAG, "No se pudo guardar PDF", ex);
                    notifyJavascript("save", false, "Error al escribir el PDF.");
                }
            } else {
                notifyJavascript("save", false, "Guardado cancelado, el PDF no se eliminó.");
            }
        }
    }

    @Override protected void onDestroy() {
        if (pendingPhotos != null) pendingPhotos.onReceiveValue(null);
        if (webView != null) webView.destroy();
        super.onDestroy();
    }
}
